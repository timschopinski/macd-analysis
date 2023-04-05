import itertools
from pandas import DataFrame
from backtesting.macd_backtest import backtest_macd
from strategies.macd import get_macd


def find_optimal_ema_parameters(
    data: DataFrame, start_amount: float = 1000
) -> tuple[int, int]:
    best_params = (12, 26)
    best_return = -float("inf")
    first_ema_range = range(5, 30)
    second_ema_range = range(10, 50)
    for params in itertools.product(first_ema_range, second_ema_range):
        first_ema, second_ema = params
        if first_ema == second_ema:
            continue
        macd_data = get_macd(
            data, short_ema_length=first_ema, long_ema_length=second_ema
        )
        total_return = backtest_macd(macd_data, start_amount=start_amount)
        if total_return > best_return:
            best_return = total_return
            best_params = params
    return best_params


def find_optimal_ema_and_signal_parameters(
    data: DataFrame, start_amount: float = 1000
) -> tuple[int, int]:
    best_params = (12, 26)
    best_return = -float("inf")
    first_ema_range = range(15, 25)
    second_ema_range = range(30, 50)
    signal_range = range(5, 20)
    for params in itertools.product(first_ema_range, second_ema_range, signal_range):
        first_ema, second_ema, signal_length = params
        if first_ema == second_ema:
            continue
        macd_data = get_macd(
            data,
            short_ema_length=first_ema,
            long_ema_length=second_ema,
            signal_length=signal_length,
        )
        total_return = backtest_macd(macd_data, start_amount=start_amount)
        if total_return > best_return:
            best_return = total_return
            best_params = params
    return best_params


if __name__ == "__main__":
    import cProfile
    from datasets.btc_data import get_data
    from utils.time_frame import TimeFrame

    data = get_data(TimeFrame.DAILY, slice_=100)
    optimal_params = find_optimal_ema_and_signal_parameters(data)
    print(optimal_params)
    # cProfile.run("find_optimal_ema_and_signal_parameters(data)")
