import pandas as pd
import pytest

from src.urbanev import assign_split, build_zone_table, occupancy_ratio


def hourly_frame(values, start="2022-12-20 00:00"):
    index = pd.date_range(start, periods=len(values), freq="h")
    return pd.DataFrame({101: values}, index=index)


def test_ratio_uses_zone_capacity():
    occupancy = hourly_frame([0.0, 5.0, 10.0])
    zones = pd.DataFrame({"charge_count": [10]}, index=[101])
    assert list(occupancy_ratio(occupancy, zones)[101]) == [0.0, 0.5, 1.0]


def test_ratio_rejects_missing_capacity():
    occupancy = hourly_frame([1.0])
    zones = pd.DataFrame({"charge_count": [0]}, index=[101])
    with pytest.raises(ValueError):
        occupancy_ratio(occupancy, zones)


def test_split_boundaries():
    hours = pd.DatetimeIndex(
        ["2022-12-31 23:00", "2023-01-01 00:00", "2023-01-31 23:00", "2023-02-01 00:00"]
    )
    assert list(assign_split(hours)) == ["train", "val", "val", "test"]


def test_features_only_see_the_past():
    ratio = hourly_frame([float(i) for i in range(200)])
    prices = {"e_price": hourly_frame([float(i) * 10 for i in range(200)])}
    table = build_zone_table(ratio, prices)
    row = table[table["occupancy_ratio"] == 180].iloc[0]
    assert row["prev_hour"] == 179
    assert row["prev_day"] == 156
    assert row["prev_week"] == 12
    assert row["mean_6h"] == sum(range(174, 180)) / 6
    assert row["e_price"] == 1790
    assert len(table) == 200 - 168
