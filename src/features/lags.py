import pandas as pd

from src.features.calendar import add_calendar_features
from src.features.weather import join_weather

MAX_LAG = 168


def build_model_table(occupancy, weather=None):
    """Saat x nokta matrisinden her satiri bir nokta ve saat olan model tablosu uretir."""
    occ = occupancy.copy()
    occ.index.name = "hour_utc"
    occ.columns.name = "stationID"

    past = occ.shift(1)
    frames = {
        "occupied": occ,
        "prev_hour": past,
        "prev_day": occ.shift(24),
        "prev_week": occ.shift(MAX_LAG),
        "mean_6h": past.rolling(6).mean(),
        "mean_24h": past.rolling(24).mean(),
    }
    columns = {name: frame.iloc[MAX_LAG:].stack() for name, frame in frames.items()}
    table = pd.concat(columns, axis=1).reset_index()

    hours = pd.DataFrame(index=occ.index[MAX_LAG:])
    extra = add_calendar_features(hours)
    if weather is not None:
        extra = join_weather(extra, weather)
    table = table.merge(extra.reset_index(), on="hour_utc", how="left")

    table["station_code"] = table["stationID"].astype("category").cat.codes
    return table
