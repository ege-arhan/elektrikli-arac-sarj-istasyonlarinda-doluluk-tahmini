"""Hava join ve sızıntı kurali testleri."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.features.weather import (  # noqa: E402
    fetch_hourly_weather,
    join_weather,
)


def test_join_weather_shift_prevents_same_hour_by_default():
    idx = pd.date_range("2020-01-01", periods=3, freq="h", tz="UTC")
    df = pd.DataFrame({"y": [0, 1, 0]}, index=idx)
    weather = pd.DataFrame(
        {"temperature_2m": [10.0, 20.0, 30.0]},
        index=idx,
    )
    out = join_weather(df, weather, shift_hours=1)
    # t=0 -> NaN, t=1 -> 10, t=2 -> 20
    assert pd.isna(out.iloc[0]["temperature_2m"])
    assert out.iloc[1]["temperature_2m"] == 10.0
    assert out.iloc[2]["temperature_2m"] == 20.0


def test_join_weather_shift0_same_hour():
    idx = pd.date_range("2020-01-01", periods=2, freq="h", tz="UTC")
    df = pd.DataFrame({"y": [0, 1]}, index=idx)
    weather = pd.DataFrame({"precipitation": [0.0, 1.5]}, index=idx)
    out = join_weather(df, weather, shift_hours=0)
    assert out.iloc[0]["precipitation"] == 0.0
    assert out.iloc[1]["precipitation"] == 1.5


def test_fetch_hourly_weather_parses_mock():
    fake = {
        "hourly": {
            "time": ["2020-01-01T00:00", "2020-01-01T01:00"],
            "temperature_2m": [10.0, 11.0],
            "precipitation": [0.0, 0.1],
            "cloud_cover": [10, 20],
        }
    }

    class FakeResp:
        def raise_for_status(self):
            return None

        def json(self):
            return fake

    with patch("src.features.weather.requests.get", return_value=FakeResp()):
        weather = fetch_hourly_weather("2020-01-01", "2020-01-01")

    assert len(weather) == 2
    assert list(weather.columns) == [
        "temperature_2m",
        "precipitation",
        "cloud_cover",
    ]
    assert weather.iloc[0]["temperature_2m"] == 10.0
