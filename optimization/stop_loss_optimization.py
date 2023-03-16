from pandas import DataFrame
from backtesting.macd_backtester import MACDTester


def get_optimized_stop_loss(data: DataFrame) -> float:
    best_stop_loss = 0
    max_return = 0
    for i in range(30):
        stop_loss = i / 100
        macd_tester = MACDTester(data, 1000, stop_loss)
        total_return = macd_tester.get_total_return()
        if total_return > max_return:
            max_return = total_return
            best_stop_loss = stop_loss

    return best_stop_loss

