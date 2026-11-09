import pandas as pd

from src.split import assign_split


def test_split_boundaries():
    hours = pd.DatetimeIndex(
        ["2019-09-30 23:00", "2019-10-01 00:00", "2020-02-29 23:00",
         "2020-03-01 00:00", "2020-10-31 23:00", "2020-11-01 00:00"],
        tz="UTC",
    )
    assert list(assign_split(hours)) == ["train", "val", "val", "masked", "masked", "test"]
