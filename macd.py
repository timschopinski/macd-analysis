import pandas as pd
import itertools

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
    data['histogram'] = data['macd'] - data['signal']
    return data


def get_macd(data: pd.DataFrame, first_ema: int = 12, second_ema: int = 26) -> pd.DataFrame:
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


def find_optimal_macd_parameters(data: pd.DataFrame, start_amount: float = 1000) -> tuple:
    best_params = (12, 26)
    best_return = -float('inf')

    first_ema_range = range(5, 30)
    second_ema_range = range(10, 50)

    for params in itertools.product(first_ema_range, second_ema_range):
        first_ema, second_ema = params
        if first_ema == second_ema:
            continue
        macd_data = get_macd(data, first_ema=first_ema, second_ema=second_ema)
        total_return = backtest_macd(macd_data, start_amount=start_amount)
        print(f'Total Return: {total_return}')
        if total_return > best_return:
            best_return = total_return
            best_params = params

    return best_params


if __name__ == '__main__':
    data = get_data()
    macd_data = get_macd(data, 29, 48)
    # data = calculate_macd_data()
    print(macd_data)
    print(macd_data['macd'])
    print(macd_data['signal'])
    print(macd_data.index.to_list()[999])
    from backtesting.macd_backtest import backtest_macd

    total_return, b, _ = backtest_macd(macd_data)
    print(b)
    print(total_return)
    # print(find_optimal_macd_parameters(data))
