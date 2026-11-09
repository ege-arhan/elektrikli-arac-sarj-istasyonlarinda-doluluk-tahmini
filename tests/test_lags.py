import pandas as pd

from src.features.lags import build_model_table


def test_lags_use_only_past():
    hours = pd.date_range("2020-01-01", periods=300, freq="h", tz="UTC")
    occ = pd.DataFrame({"A": [i % 2 for i in range(300)], "B": 0}, index=hours)
    table = build_model_table(occ)

    row = table[(table["stationID"] == "A") & (table["hour_utc"] == hours[200])].iloc[0]
    assert row["occupied"] == occ.loc[hours[200], "A"]
    assert row["prev_hour"] == occ.loc[hours[199], "A"]
    assert row["prev_week"] == occ.loc[hours[200 - 168], "A"]
    assert row["mean_6h"] == occ["A"].iloc[194:200].mean()
    assert len(table) == (300 - 168) * 2
