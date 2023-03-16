import pandas as pd
from pandas import DataFrame
from utils.time_frame import TimeFrame
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def get_data_set(time_frame: TimeFrame) -> Path:
    """
    Returns path to a dataset with a given timeframe
    """

    datasets = {
        TimeFrame.DAILY: BASE_DIR / 'datasets/BTC-Daily.csv',
        TimeFrame.HOURLY: BASE_DIR / 'datasets/BTC-Hourly.csv',
    }
    return datasets[time_frame]


def get_data(
        time_frame: TimeFrame,
        date_from: str | None = None,
        date_to: str | None = None,
        slice_: int | None = None,
        reverse: bool = True
) -> DataFrame:
    """
    Returns BTC/USD data as pandas.DataFrame containing
    unix, date, symbol, open, high, low, close, Volume BTC, Volume USD
    """
    data = pd.read_csv(get_data_set(time_frame), parse_dates=['date'], index_col=['date'])
    if date_from:
        mask = (data.index >= date_from)
        data = data.loc[mask]
    if date_to:
        mask = (data.index <= date_to)
        data = data.loc[mask]
    if slice_:
        data = data.head(slice_)
    if reverse:
        return data[::-1]
    return data

