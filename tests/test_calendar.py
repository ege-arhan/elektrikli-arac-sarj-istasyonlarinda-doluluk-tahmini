"""Takvim ozellikleri icin kucuk kontroller."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.features.calendar import add_calendar_features  # noqa: E402


def test_holiday_and_weekend_and_academic_break():
    idx = pd.DatetimeIndex(
        [
            "2020-07-04 18:00:00+00:00",  # bagimsizlik gunu (LA hala 4 Temmuz)
            "2020-07-05 18:00:00+00:00",  # pazar
            "2020-12-20 18:00:00+00:00",  # kis ara 2020-21
            "2020-01-15 18:00:00+00:00",  # normal carsamba
        ],
        tz="UTC",
    )
    df = pd.DataFrame({"x": [1, 2, 3, 4]}, index=idx)
    out = add_calendar_features(df)

    assert out.loc[idx[0], "is_holiday"] == 1
    assert out.loc[idx[1], "is_weekend_local"] == 1
    assert out.loc[idx[2], "is_academic_break"] == 1
    assert out.loc[idx[3], "is_holiday"] == 0
    assert out.loc[idx[3], "is_academic_break"] == 0
    assert out.loc[idx[3], "is_weekend_local"] == 0
    assert "hour_local" in out.columns
    assert "day_of_week_local" in out.columns
