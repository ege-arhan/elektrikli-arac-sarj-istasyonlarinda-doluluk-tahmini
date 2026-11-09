from pathlib import Path

import holidays
import pandas as pd

MAX_LAG = 168
PRICE_COLUMNS = ("e_price", "s_price")

TRAIN_END = pd.Timestamp("2022-12-31 23:00")
VAL_END = pd.Timestamp("2023-01-31 23:00")


def load_zone_tables(urbanev_dir: Path) -> dict[str, pd.DataFrame]:
    """Bolge duzeyi saatlik doluluk, fiyat ve kapasite tablolarini okur."""
    base = Path(urbanev_dir) / "20220901-20230228_zone-cleaned-aggregated"
    tables = {}
    for name in ("occupancy", *PRICE_COLUMNS):
        table = pd.read_csv(base / "charge_1hour" / f"{name}.csv", index_col=0, parse_dates=True)
        table.columns = table.columns.astype(int)
        tables[name] = table.sort_index()
    tables["zones"] = pd.read_csv(base / "zone-information.csv").set_index("TAZID")
    return tables


def occupancy_ratio(occupancy: pd.DataFrame, zones: pd.DataFrame) -> pd.DataFrame:
    """Dolu nokta sayisini bolge kapasitesine bolerek orana cevirir."""
    capacity = zones["charge_count"].reindex(occupancy.columns)
    if capacity.isna().any() or capacity.le(0).any():
        raise ValueError("her bolge icin pozitif kapasite gerekli")
    return occupancy.div(capacity, axis=1)


def assign_split(hours: pd.DatetimeIndex) -> pd.Series:
    """Saatleri kronolojik olarak train, val ve test olarak ayirir."""
    split = pd.Series("test", index=hours)
    split.loc[hours <= VAL_END] = "val"
    split.loc[hours <= TRAIN_END] = "train"
    return split


def build_zone_table(ratio: pd.DataFrame, prices: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Her satiri bir bolge ve saat olan tablo uretir. Ozellikler yalniz gecmisi gorur."""
    occ = ratio.copy()
    occ.index.name = "hour"
    occ.columns.name = "zone"

    past = occ.shift(1)
    frames = {
        "occupancy_ratio": occ,
        "prev_hour": past,
        "prev_day": occ.shift(24),
        "prev_week": occ.shift(MAX_LAG),
        "mean_6h": past.rolling(6).mean(),
        "mean_24h": past.rolling(24).mean(),
    }
    for name, table in prices.items():
        frames[name] = table.shift(1)
    columns = {name: frame.iloc[MAX_LAG:].stack() for name, frame in frames.items()}
    table = pd.concat(columns, axis=1)
    table.index.names = ["hour", "zone"]
    table = table.reset_index()

    hours = occ.index[MAX_LAG:]
    china = holidays.CN(years=sorted(set(hours.year)))
    calendar = pd.DataFrame(
        {
            "hour_local": hours.hour,
            "day_of_week": hours.dayofweek,
            "is_weekend": (hours.dayofweek >= 5).astype(int),
            "is_holiday": [int(day in china) for day in hours.date],
            "split": assign_split(hours).to_numpy(),
        },
        index=hours,
    )
    return table.merge(calendar, left_on="hour", right_index=True, how="left")
