import pandas as pd


def get_data():
    data = pd.read_csv('datasets/BTC-Daily.csv', parse_dates=['date'], index_col='date')
    return data
