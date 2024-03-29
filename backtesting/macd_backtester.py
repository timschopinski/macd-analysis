from typing import List
from pandas import DataFrame, Timestamp
from backtesting.stop_loss import StopLossManager, StopLossOrder
from models.transaction import Transaction, TransactionType
from logger.logger import TransactionLogger
from backtesting.buy_and_sell_level import BuyAndSellLevelManager


class MACDTester:
    def __init__(
        self,
        data: DataFrame,
        start_amount: float = 1000,
        stop_loss: float | None = None,
        commission: float = 0,
        macd_buy_level: float | None = None,
        macd_sell_level: float | None = None,
    ):
        self.data = data
        self.start_amount = start_amount
        self.transactions: List[Transaction] = []
        self.capital = start_amount
        self.asset_amount = 0
        self.stop_loss_manager = StopLossManager(stop_loss)
        self.num_of_transactions = 0
        self.commission_rate = commission
        self.total_commission = 0
        if macd_buy_level and macd_sell_level:
            self.level_manager = BuyAndSellLevelManager(
                macd_buy_level=macd_buy_level,
                macd_sell_level=macd_sell_level,
            )
        else:
            self.level_manager = None

    def get_sell_dates(self) -> List[Timestamp]:
        sell_transactions = filter(
            lambda x: x.type == TransactionType.SELL, self.transactions
        )
        return list(map(lambda transaction: transaction.date, sell_transactions))

    def get_buy_dates(self) -> List[Timestamp]:
        buy_transactions = filter(
            lambda x: x.type == TransactionType.BUY, self.transactions
        )
        return list(map(lambda transaction: transaction.date, buy_transactions))

    def get_sell_prices(self) -> List[float]:
        sell_transactions = filter(
            lambda x: x.type == TransactionType.SELL, self.transactions
        )
        return list(map(lambda transaction: transaction.price, sell_transactions))

    def get_buy_prices(self) -> List[float]:
        buy_transactions = filter(
            lambda x: x.type == TransactionType.BUY, self.transactions
        )
        return list(map(lambda transaction: transaction.price, buy_transactions))

    def get_transaction_profits(self) -> DataFrame:
        profits = [transaction.profit for transaction in self.transactions]
        return DataFrame(profits, columns=["Profit/Loss"])

    def _finish_transaction_details(self, price: float) -> None:
        self.stop_loss_manager.set_recent_action_price(price)
        self.num_of_transactions += 1

    def _get_recent_transaction(self) -> Transaction | None:
        if self.transactions:
            return self.transactions[-1]
        return None

    def validate_transaction_level(
        self, macd: DataFrame, transaction_type: TransactionType
    ) -> bool:
        if self.level_manager is None:
            return True
        else:
            if self.level_manager.check_level(macd, transaction_type):
                return True
        return False

    def _buy(self, date: Timestamp, price: float) -> bool:
        self.asset_amount = self.capital / price
        self.asset_amount = self.asset_amount - self.asset_amount * self.commission_rate
        self.total_commission += self.commission_rate * self.asset_amount * price
        recent_transaction = self._get_recent_transaction()
        if recent_transaction:
            profit = (
                self.asset_amount * price
                - recent_transaction.price * recent_transaction.amount
            )
        else:
            profit = 0
        self.transactions.append(
            Transaction(date, price, self.asset_amount, profit, TransactionType.BUY)
        )
        self.capital = 0
        self._finish_transaction_details(price)
        return True

    def _sell(self, date: Timestamp, price: float) -> bool:
        self.capital = self.asset_amount * price
        self.capital = self.capital - self.commission_rate * self.capital
        self.total_commission += self.commission_rate * self.capital
        recent_transaction = self._get_recent_transaction()
        if recent_transaction:
            profit = self.capital - recent_transaction.price * recent_transaction.amount
        else:
            profit = 0
        self.transactions.append(
            Transaction(date, price, self.asset_amount, profit, TransactionType.SELL)
        )
        self.asset_amount = 0
        self._finish_transaction_details(price)
        return False

    def get_total_return(self) -> float:
        holding = False
        close_price = 0
        for i in range(len(self.data)):
            date = self.data.index[i]
            row = self.data.iloc[i]
            histogram = row["histogram"]
            close_price = row["close"]
            macd = row["macd"]
            stop_loss_order = self.stop_loss_manager.get_order(close_price, holding)
            if (
                stop_loss_order == StopLossOrder.SELL
                and self.validate_transaction_level(macd, TransactionType.SELL)
            ):
                holding = self._sell(date, close_price)
            elif (
                histogram > 0
                and not holding
                and self.validate_transaction_level(macd, TransactionType.BUY)
            ):
                holding = self._buy(date, close_price)
            elif (
                histogram < 0
                and holding
                and self.validate_transaction_level(macd, TransactionType.SELL)
            ):
                holding = self._sell(date, close_price)
        if self.capital:
            total_return = self.capital - self.start_amount
        else:
            total_return = self.asset_amount * close_price - self.start_amount
        return total_return


if __name__ == "__main__":
    from datasets.btc_data import get_data
    from strategies.macd import get_macd
    from utils.time_frame import TimeFrame

    data = get_data(TimeFrame.DAILY, date_from="2019-06-07", date_to="2022-03-01")
    print(data)
    macd_data = get_macd(data, 29, 48)
    macd_tester = MACDTester(macd_data)
    print(f"Total return: {macd_tester.get_total_return()}$")
    logger = TransactionLogger()
    logger.log_transactions_info(macd_tester.transactions)
