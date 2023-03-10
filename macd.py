import pandas as pd

from btc_data import get_data


def calculate_macd_data(n1: int = 12, n2: int = 26):
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
    return data


def get_macd(data: pd.DataFrame) -> pd.DataFrame:
    ema12 = data['close'].ewm(span=12, adjust=False).mean()
    ema26 = data['close'].ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    data['ema12'] = ema12
    data['ema26'] = ema26
    data['macd'] = macd
    data['signal'] = signal

    return data


if __name__ == '__main__':
    data = get_macd(get_data().head(100).copy())
    print(data)
    print(data['macd'])
    print(data['signal'])
