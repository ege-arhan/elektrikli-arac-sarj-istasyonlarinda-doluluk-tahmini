"""Caltech ACN oturumlarini okur ve saatlik doluluk matrisi uretir."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

EXPECTED_QUARTER_COUNTS = {
    "caltech_2018_Q2.json": 3880,
    "caltech_2018_Q3.json": 6793,
    "caltech_2018_Q4.json": 4624,
    "caltech_2019_Q1.json": 2876,
    "caltech_2019_Q2.json": 2884,
    "caltech_2019_Q3.json": 2508,
    "caltech_2019_Q4.json": 2349,
    "caltech_2020_Q1.json": 2051,
    "caltech_2020_Q2.json": 81,
    "caltech_2020_Q3.json": 71,
    "caltech_2020_Q4.json": 269,
    "caltech_2021_Q1.json": 614,
    "caltech_2021_Q2.json": 1085,
    "caltech_2021_Q3.json": 1339,
}

TIME_COLUMNS = ["connectionTime", "disconnectTime", "doneChargingTime"]
ID_COLUMNS = ["sessionID", "stationID", "siteID"]


def default_acn_dir(project_dir: Path | None = None) -> Path:
    if project_dir is None:
        project_dir = Path.cwd()
        if project_dir.name == "notebooks":
            project_dir = project_dir.parent
    return Path(project_dir) / "data" / "raw" / "acn"


def occupied_hours_for_session(
    connection_utc: pd.Timestamp, disconnect_utc: pd.Timestamp
) -> list[pd.Timestamp]:
    """Baglanti ceil(h) ile baslar ayrilma ceil(h) den onceki saat baslarina 1 yazilir."""
    hour = connection_utc.ceil("h")
    end_hour = disconnect_utc.ceil("h")
    hours: list[pd.Timestamp] = []
    while hour < end_hour:
        hours.append(hour)
        hour = hour + pd.Timedelta(hours=1)
    return hours


def load_caltech_sessions(
    data_dir: Path | None = None,
    *,
    check_expected_counts: bool = True,
) -> pd.DataFrame:
    data_dir = Path(data_dir) if data_dir is not None else default_acn_dir()
    json_files = sorted(data_dir.glob("caltech_*.json"))
    if len(json_files) != 14:
        raise FileNotFoundError(
            f"14 caltech_*.json bekleniyordu {data_dir} icinde {len(json_files)} bulundu"
        )

    all_sessions: list[dict] = []
    for file_path in json_files:
        with file_path.open(encoding="utf-8") as file:
            quarter_data = json.load(file)
        quarter_sessions = quarter_data["_items"]
        if check_expected_counts:
            expected = EXPECTED_QUARTER_COUNTS[file_path.name]
            if len(quarter_sessions) != expected:
                raise ValueError(
                    f"{file_path.name}: {len(quarter_sessions)} oturum var beklenen {expected}"
                )
        for session in quarter_sessions:
            row = dict(session)
            row["_source_file"] = file_path.name
            all_sessions.append(row)

    sessions = pd.DataFrame(all_sessions)
    for column in TIME_COLUMNS:
        sessions[f"{column}_utc"] = pd.to_datetime(
            sessions[column], utc=True, errors="coerce"
        )

    sessions = sessions.sort_values("connectionTime_utc").reset_index(drop=True)
    return sessions


def session_quality_report(sessions: pd.DataFrame) -> dict[str, int]:
    missing_times = sessions[["connectionTime_utc", "disconnectTime_utc"]].isna().any(
        axis=1
    )
    invalid_intervals = (
        sessions["disconnectTime_utc"] <= sessions["connectionTime_utc"]
    )
    duplicate_ids = sessions["sessionID"].duplicated()

    missing_ids = {
        column: int(sessions[column].isna().sum() + (sessions[column] == "").sum())
        if column in sessions.columns
        else int(len(sessions))
        for column in ID_COLUMNS
    }

    return {
        "missing_times": int(missing_times.sum()),
        "invalid_intervals": int(invalid_intervals.sum()),
        "duplicate_session_ids": int(duplicate_ids.sum()),
        "missing_sessionID": missing_ids["sessionID"],
        "missing_stationID": missing_ids["stationID"],
        "missing_siteID": missing_ids["siteID"],
        "n_sessions": int(len(sessions)),
        "n_stations": int(sessions["stationID"].nunique()),
    }


def find_overlapping_sessions(sessions: pd.DataFrame) -> pd.DataFrame:
    """Ayni stationID uzerinde zaman araligi cakisan oturum ciftlerini bulur."""
    required = ["sessionID", "stationID", "connectionTime_utc", "disconnectTime_utc"]
    work = sessions[required].dropna().copy()
    work = work.sort_values(["stationID", "connectionTime_utc", "disconnectTime_utc"])

    overlaps: list[dict] = []
    for station_id, group in work.groupby("stationID", sort=False):
        rows = group.reset_index(drop=True)
        active: list[dict] = []
        for row in rows.itertuples(index=False):
            current = {
                "sessionID": row.sessionID,
                "connectionTime_utc": row.connectionTime_utc,
                "disconnectTime_utc": row.disconnectTime_utc,
            }
            still_active = []
            for prev in active:
                if prev["disconnectTime_utc"] > current["connectionTime_utc"]:
                    overlaps.append(
                        {
                            "stationID": station_id,
                            "sessionID_a": prev["sessionID"],
                            "sessionID_b": current["sessionID"],
                            "a_connection": prev["connectionTime_utc"],
                            "a_disconnect": prev["disconnectTime_utc"],
                            "b_connection": current["connectionTime_utc"],
                            "b_disconnect": current["disconnectTime_utc"],
                        }
                    )
                    still_active.append(prev)
            active = still_active
            active.append(current)

    return pd.DataFrame(overlaps)


def build_occupancy_matrix(sessions: pd.DataFrame) -> pd.DataFrame:
    occupied_rows: list[dict] = []
    for session in sessions.itertuples():
        for hour in occupied_hours_for_session(
            session.connectionTime_utc, session.disconnectTime_utc
        ):
            occupied_rows.append(
                {
                    "hour_utc": hour,
                    "stationID": session.stationID,
                    "occupied": 1,
                }
            )

    if not occupied_rows:
        station_ids = sorted(sessions["stationID"].dropna().unique())
        return pd.DataFrame(columns=station_ids)

    occupied_hours = pd.DataFrame(occupied_rows)
    occupancy_matrix = occupied_hours.pivot_table(
        index="hour_utc",
        columns="stationID",
        values="occupied",
        aggfunc="max",
    )

    all_hours = pd.date_range(
        start=sessions["connectionTime_utc"].min().floor("h"),
        end=sessions["disconnectTime_utc"].max().ceil("h"),
        freq="h",
        inclusive="left",
    )
    station_ids = sorted(sessions["stationID"].dropna().unique())
    occupancy_matrix = occupancy_matrix.reindex(index=all_hours, columns=station_ids)
    return occupancy_matrix.fillna(0).astype(int)
