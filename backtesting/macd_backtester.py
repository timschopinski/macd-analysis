from typing import List, NamedTuple
from pandas import DataFrame, Timestamp
from backtesting.stop_loss import StopLossManager, StopLossOrder


class Point(NamedTuple):
    """
    This class represents a Point
    with a date as x value and price as y value
    """
    date: Timestamp
    price: float


class MACDTester:

    def __init__(
        self,
        data: DataFrame,
        start_amount: float = 1000,
        stop_loss: float | None = None
    ):
        self.data = data
        self.start_amount = start_amount
        self.buy_points: List[Point] = []
        self.sell_points: List[Point] = []
        self.capital = start_amount
        self.asset_amount = 0
        self.stop_loss_manager = StopLossManager(stop_loss)

    def get_sell_dates(self) -> List[Timestamp]:
        return list(map(lambda point: point.date, self.sell_points))

    def get_buy_dates(self) -> List[Timestamp]:
        return list(map(lambda point: point.date, self.buy_points))

    def get_sell_prices(self) -> List[float]:
        return list(map(lambda point: point.price, self.sell_points))

    def get_buy_prices(self) -> List[float]:
        return list(map(lambda point: point.price, self.buy_points))

    def _buy(self, date: Timestamp, price: float) -> bool:
        self.asset_amount = self.capital / price
        self.capital = 0
        self.buy_points.append(Point(date, price))
        self.stop_loss_manager.set_recent_action_price(price)
        return True

    def _sell(self, date: Timestamp, price: float) -> bool:
        self.capital = self.asset_amount * price
        self.asset_amount = 0
        self.sell_points.append(Point(date, price))
        self.stop_loss_manager.set_recent_action_price(price)
        return False

    def get_total_return(self) -> float:
        """
        Returns a total_return after backtesting
        """
        holding = False
        close_price = 0
        for i in range(len(self.data)):
            date = self.data.index[i]
            row = self.data.iloc[i]
            macd = row['macd']
            close_price = row['close']
            signal = row['signal']
            stop_loss_order = self.stop_loss_manager.get_order(close_price, holding)
            if stop_loss_order == StopLossOrder.SELL:
                holding = self._sell(date, close_price)
            elif macd > signal and not holding:
                holding = self._buy(date, close_price)
            elif macd < signal and holding:
                holding = self._sell(date, close_price)
        if self.capital:
            total_return = self.capital - self.start_amount
        else:
            total_return = self.asset_amount * close_price - self.start_amount

        return total_return
