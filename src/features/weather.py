"""Open-Meteo ile Caltech saatlik gecmis hava.

Tek konum (kampus). UTC saatlik tablo uretir.
Bir saat ileri doluluk tahmini icin varsayilan join shift_hours=1:
index saati t iken hava t-1 kullanilir (t+1 gercek hava sizintisi yok).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

# Caltech / Pasadena yakini
CALTECH_LAT = 34.1377
CALTECH_LON = -118.1253

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
HOURLY_VARS = ("temperature_2m", "precipitation", "cloud_cover")


def default_weather_path(project_dir: Path | None = None) -> Path:
    if project_dir is None:
        project_dir = Path.cwd()
        if project_dir.name == "notebooks":
            project_dir = project_dir.parent
    return Path(project_dir) / "data" / "processed" / "caltech_weather_hourly.csv"


def fetch_hourly_weather(
    start_date: str,
    end_date: str,
    *,
    latitude: float = CALTECH_LAT,
    longitude: float = CALTECH_LON,
    timeout: int = 120,
) -> pd.DataFrame:
    """Open-Meteo archive API'den saatlik hava ceker. Tarihler YYYY-MM-DD."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(HOURLY_VARS),
        "timezone": "UTC",
    }
    response = requests.get(ARCHIVE_URL, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    hourly = payload.get("hourly") or {}
    if "time" not in hourly:
        raise ValueError(f"Open-Meteo hourly.time yok: {payload.keys()}")

    weather = pd.DataFrame({"hour_utc": pd.to_datetime(hourly["time"], utc=True)})
    for name in HOURLY_VARS:
        weather[name] = hourly.get(name)
    weather = weather.set_index("hour_utc").sort_index()
    weather.attrs["latitude"] = latitude
    weather.attrs["longitude"] = longitude
    return weather


def save_weather(weather: pd.DataFrame, path: Path | None = None) -> Path:
    path = default_weather_path() if path is None else Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    out = weather.reset_index()
    out.to_csv(path, index=False)
    return path


def load_weather(path: Path | None = None) -> pd.DataFrame:
    path = default_weather_path() if path is None else Path(path)
    weather = pd.read_csv(path, parse_dates=["hour_utc"])
    weather["hour_utc"] = pd.to_datetime(weather["hour_utc"], utc=True)
    return weather.set_index("hour_utc").sort_index()


def join_weather(
    df: pd.DataFrame,
    weather: pd.DataFrame,
    *,
    shift_hours: int = 1,
    columns: tuple[str, ...] | None = None,
) -> pd.DataFrame:
    """DatetimeIndex'li tabloya hava kolonlarini ekler.

    shift_hours=1 (varsayilan): t satirina weather[t-1] gelir.
    shift_hours=0: ayni saat havasi (egitimde siziinti riski daha yuksek).
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("df index DatetimeIndex olmali")

    cols = list(columns) if columns is not None else [
        c for c in HOURLY_VARS if c in weather.columns
    ]
    aligned = weather[cols].copy()
    if shift_hours:
        aligned = aligned.shift(shift_hours)

    # index tz uyumu
    left = df.copy()
    if left.index.tz is None:
        left.index = left.index.tz_localize("UTC")
    else:
        left.index = left.index.tz_convert("UTC")

    if aligned.index.tz is None:
        aligned.index = aligned.index.tz_localize("UTC")
    else:
        aligned.index = aligned.index.tz_convert("UTC")

    joined = left.join(aligned, how="left")
    return joined
