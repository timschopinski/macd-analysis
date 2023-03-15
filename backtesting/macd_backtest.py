from typing import List, NamedTuple
from pandas import DataFrame


class Point(NamedTuple):
    """
    This class represents a Point
    with a date as x value and price as y value
    """
    date: str
    price: float


def backtest_macd(
        data: DataFrame,
        start_amount: float = 1000
) -> tuple[float, List[Point], List[Point]]:
    """
    Returns a tuple containing total_return, buy_points and sell_points
    """
    holding = False
    capital = start_amount
    asset_amount, close_price = 0, 0
    buy_points: List[Point] = []
    sell_points: List[Point] = []

    for i in range(len(data)):
        date = data.index[i]
        row = data.iloc[i]
        macd = row['macd']
        close_price = row['close']
        signal = row['signal']
        if macd > signal and not holding:
            asset_amount = capital / close_price
            capital = 0
            holding = True
            buy_points.append(Point(date, close_price))
        elif macd < signal and holding:
            capital = asset_amount * close_price
            asset_amount = 0
            holding = False
            sell_points.append(Point(date, close_price))

    if capital:
        total_return = capital - start_amount
    else:
        total_return = asset_amount * close_price - start_amount

    return total_return, buy_points, sell_points
