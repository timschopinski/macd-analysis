import pandas as pd
from pandas import DataFrame

from datasets.btc_data import get_data
from backtesting.macd_backtester import MACDTester


def calculate_macd_data(n1: int = 12, n2: int = 26) -> DataFrame:
    data = get_data()[['close']].copy()
    data = data.head(1000)

    signal_length = 9

    def calculate_ema(window):
        meter = 0
        denominator = 0
        n = len(window) - 1
        alpha = 2 / (n + 1)

        for index, p in enumerate(window[::-1]):
            meter += p * (1 - alpha) ** index
            denominator += (1 - alpha) ** index
        ema = meter / denominator
        return ema

    data['ema1'] = data['close'].rolling(n1+1).apply(calculate_ema)
    data['ema2'] = data['close'].rolling(n2+1).apply(calculate_ema)
    data['macd'] = data['ema1'] - data['ema2']
    data.dropna(subset=['macd'], inplace=True)
    data['signal'] = data['macd'].rolling(signal_length+1).apply(calculate_ema)
    data.dropna(subset=['signal'], inplace=True)
    data['histogram'] = data['macd'] - data['signal']
    return data


def get_macd(data: DataFrame, first_ema: int = 12, second_ema: int = 26) -> DataFrame:
    first_ema_data = data['close'].ewm(span=first_ema, adjust=False).mean()
    second_ema_data = data['close'].ewm(span=second_ema, adjust=False).mean()

    macd = first_ema_data - second_ema_data
    signal = macd.ewm(span=9, adjust=False).mean()

    data[f'ema{first_ema}'] = first_ema_data
    data[f'ema{second_ema}'] = second_ema_data
    data['macd'] = macd
    data['signal'] = signal
    data['histogram'] = data['macd'] - data['signal']
    return data


if __name__ == '__main__':
    data = get_data()
    macd_data = get_macd(data, 29, 48)
    # data = calculate_macd_data()
    print(macd_data)

    macd_tester = MACDTester(data)
    total_return = macd_tester.get_total_return()
    print(total_return)
