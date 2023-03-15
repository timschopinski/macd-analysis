import itertools
from pandas import DataFrame
from backtesting.macd_backtest import backtest_macd
from strategies.macd import get_macd


def find_optimal_macd_parameters(data: DataFrame, start_amount: float = 1000) -> tuple:
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
