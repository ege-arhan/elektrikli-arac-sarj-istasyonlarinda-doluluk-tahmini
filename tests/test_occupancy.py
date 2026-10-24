"""Saatlik doluluk kurali icin kucuk ornek testleri."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.load_data import (  # noqa: E402
    build_occupancy_matrix,
    find_overlapping_sessions,
    occupied_hours_for_session,
)


def _ts(text: str) -> pd.Timestamp:
    return pd.Timestamp(text, tz="UTC")


def test_normal_session_hours():
    # 18:10 - 21:05 -> 19 20 21
    hours = occupied_hours_for_session(
        _ts("2020-01-15 18:10:00"), _ts("2020-01-15 21:05:00")
    )
    assert [h.hour for h in hours] == [19, 20, 21]


def test_overnight_session_hours():
    hours = occupied_hours_for_session(
        _ts("2020-01-15 22:30:00"), _ts("2020-01-16 01:15:00")
    )
    assert [h.strftime("%Y-%m-%d %H:%M") for h in hours] == [
        "2020-01-15 23:00",
        "2020-01-16 00:00",
        "2020-01-16 01:00",
    ]


def test_exact_hour_boundaries():
    # tam saat basinda: 10:00-12:00 -> 10 ve 11 (ceil kurali)
    hours = occupied_hours_for_session(
        _ts("2020-01-15 10:00:00"), _ts("2020-01-15 12:00:00")
    )
    assert [h.hour for h in hours] == [10, 11]

    # tam bir saat: 10:00-11:00 -> sadece 10
    hours_one = occupied_hours_for_session(
        _ts("2020-01-15 10:00:00"), _ts("2020-01-15 11:00:00")
    )
    assert [h.hour for h in hours_one] == [10]


def test_short_session_no_hour_crossed():
    # ayni saat icinde biten kisa oturum hic saat basi uretmez
    hours = occupied_hours_for_session(
        _ts("2020-01-15 10:10:00"), _ts("2020-01-15 10:40:00")
    )
    assert hours == []


def test_invalid_interval_yields_no_hours():
    hours = occupied_hours_for_session(
        _ts("2020-01-15 12:00:00"), _ts("2020-01-15 11:00:00")
    )
    assert hours == []


def test_dst_spring_forward_local_note():
    # utc araligi duzgun kalsin yaz saati gecisinde de saat basi listesi surekli olsun
    hours = occupied_hours_for_session(
        _ts("2020-03-08 08:30:00"), _ts("2020-03-08 11:10:00")
    )
    assert [h.hour for h in hours] == [9, 10, 11]


def test_build_occupancy_matrix_and_overlap():
    sessions = pd.DataFrame(
        [
            {
                "sessionID": "a",
                "stationID": "s1",
                "connectionTime_utc": _ts("2020-01-01 10:10:00"),
                "disconnectTime_utc": _ts("2020-01-01 12:05:00"),
            },
            {
                "sessionID": "b",
                "stationID": "s1",
                "connectionTime_utc": _ts("2020-01-01 11:30:00"),
                "disconnectTime_utc": _ts("2020-01-01 13:00:00"),
            },
            {
                "sessionID": "c",
                "stationID": "s2",
                "connectionTime_utc": _ts("2020-01-01 10:00:00"),
                "disconnectTime_utc": _ts("2020-01-01 11:00:00"),
            },
        ]
    )

    overlaps = find_overlapping_sessions(sessions)
    assert len(overlaps) == 1
    assert set(overlaps.loc[0, ["sessionID_a", "sessionID_b"]]) == {"a", "b"}

    matrix = build_occupancy_matrix(sessions)
    assert matrix.loc[_ts("2020-01-01 11:00:00"), "s1"] == 1
    assert matrix.loc[_ts("2020-01-01 12:00:00"), "s1"] == 1
    # b 13:00 tam ayrildigi icin 13:00 satiri inclusive left aralikta yok
    assert matrix.index.max() == _ts("2020-01-01 12:00:00")


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
