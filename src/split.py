import pandas as pd

TRAIN_START = pd.Timestamp("2018-05-01 00:00", tz="UTC")
TRAIN_END = pd.Timestamp("2019-09-30 23:00", tz="UTC")
VAL_START = pd.Timestamp("2019-10-01 00:00", tz="UTC")
VAL_END = pd.Timestamp("2020-02-29 23:00", tz="UTC")
TEST_START = pd.Timestamp("2020-11-01 00:00", tz="UTC")
TEST_END = pd.Timestamp("2021-09-14 23:00", tz="UTC")


def assign_split(hours):
    """Her saate train, val, test ya da masked yazar. 2020-03..2020-10 kayit bosluğu masked."""
    split = pd.Series("masked", index=hours)
    split.loc[(hours >= TRAIN_START) & (hours <= TRAIN_END)] = "train"
    split.loc[(hours >= VAL_START) & (hours <= VAL_END)] = "val"
    split.loc[(hours >= TEST_START) & (hours <= TEST_END)] = "test"
    return split
