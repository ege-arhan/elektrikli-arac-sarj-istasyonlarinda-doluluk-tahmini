"""Takvim ve tatil ozellikleri (Los Angeles yerel).

Resmi tatiller holidays.US(state=CA) ile uretilir.
Akademik ara donemler Caltech registrar / kampus takviminden
derlenen tarih araliklaridir; bazi yaz araliklari yaklasiktir.
"""

from __future__ import annotations

from datetime import date, timedelta

import holidays
import pandas as pd

# inclusive [start, end] America/Los_Angeles yerel tarih
# kaynak: registrar 2020-21 PDF; 2019-20 kis ara kampus etkinligi;
# diger yillar ayni donem yapisina gore yaklasik
CALTECH_ACADEMIC_BREAKS: list[tuple[date, date, str]] = [
    (date(2018, 6, 15), date(2018, 9, 24), "summer_approx"),
    (date(2018, 12, 15), date(2019, 1, 6), "winter_approx"),
    (date(2019, 3, 18), date(2019, 3, 24), "spring_approx"),
    (date(2019, 6, 15), date(2019, 9, 29), "summer_approx"),
    (date(2019, 12, 14), date(2020, 1, 5), "winter_documented"),
    (date(2020, 3, 21), date(2020, 3, 29), "spring_approx"),
    (date(2020, 6, 13), date(2020, 9, 27), "summer_approx"),
    (date(2020, 12, 12), date(2021, 1, 3), "winter_2020_21"),
    (date(2021, 3, 18), date(2021, 3, 28), "spring_2020_21"),
    (date(2021, 6, 12), date(2021, 9, 30), "summer_approx"),
]


def _daterange_set(ranges: list[tuple[date, date, str]]) -> set[date]:
    days: set[date] = set()
    for start, end, _label in ranges:
        cur = start
        while cur <= end:
            days.add(cur)
            cur += timedelta(days=1)
    return days


ACADEMIC_BREAK_DAYS = _daterange_set(CALTECH_ACADEMIC_BREAKS)


def _local_timestamps(ts: pd.Series, local_tz: str) -> pd.Series:
    times = pd.to_datetime(ts, utc=True)
    if times.dt.tz is None:
        times = times.dt.tz_localize("UTC")
    return times.dt.tz_convert(local_tz)


def add_calendar_features(
    df: pd.DataFrame,
    ts_col: str | None = None,
    *,
    local_tz: str = "America/Los_Angeles",
    country: str = "US",
    state: str | None = "CA",
) -> pd.DataFrame:
    """Saatlik tabloya yerel takvim kolonlari ekler.

    ts_col None ise index DatetimeIndex kabul edilir.
    """
    out = df.copy()
    if ts_col is None:
        if not isinstance(out.index, pd.DatetimeIndex):
            raise TypeError("ts_col yoksa index DatetimeIndex olmali")
        local = out.index.tz_convert(local_tz) if out.index.tz is not None else out.index.tz_localize("UTC").tz_convert(local_tz)
        local = pd.DatetimeIndex(local)
    else:
        local = _local_timestamps(out[ts_col], local_tz)

    out["hour_local"] = local.hour
    out["day_of_week_local"] = local.dayofweek
    out["is_weekend_local"] = (local.dayofweek >= 5).astype(int)
    out["month_local"] = local.month

    years = range(int(local.year.min()), int(local.year.max()) + 1)
    if country != "US":
        raise ValueError("bu proje icin su an sadece US/CA tatilleri tanimli")
    # holidays 0.106+: state yerine subdiv
    cal = holidays.US(years=years, subdiv=state) if state else holidays.US(years=years)

    local_dates = pd.Series(local.date, index=out.index)
    out["is_holiday"] = local_dates.map(lambda d: int(d in cal))
    out["is_academic_break"] = local_dates.map(
        lambda d: int(d in ACADEMIC_BREAK_DAYS)
    )
    return out
