from typing import List, Iterable
from models.transaction import Transaction
import logging


class TransactionLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def get_worst_transaction(transactions: Iterable[Transaction]) -> Transaction:
        min_profit_transaction = None
        min_profit = float("+inf")

        for transaction in transactions:
            if transaction.profit < min_profit:
                min_profit = transaction.profit
                min_profit_transaction = transaction

        return min_profit_transaction

    @staticmethod
    def get_best_transaction(transactions: Iterable[Transaction]) -> Transaction:
        max_profit_transaction = None
        max_profit = float("-inf")

        for transaction in transactions:
            if transaction.profit > max_profit:
                max_profit = transaction.profit
                max_profit_transaction = transaction

        return max_profit_transaction

    def log_best_transaction(self, transactions: Iterable[Transaction]) -> None:
        self.logger.info(f"Best transaction: {self.get_best_transaction(transactions)}")

    def log_worst_transaction(self, transactions: Iterable[Transaction]) -> None:
        self.logger.warning(
            f"Worst transaction: {self.get_worst_transaction(transactions)}"
        )

    def log_profitable_transactions(self, transactions: Iterable[Transaction]):
        profitable_transactions = [t for t in transactions if t.profit > 0]
        self.logger.info(
            f"Number of profitable transactions: {len(profitable_transactions)}"
        )

    def log_unprofitable_transactions(self, transactions: Iterable[Transaction]):
        unprofitable_transactions = [t for t in transactions if t.profit < 0]
        self.logger.warning(
            f"Number of unprofitable transactions: {len(unprofitable_transactions)}"
        )

    def log_all_transactions(self, transactions: Iterable[Transaction]):
        self.logger.info("All transactions:")
        for transaction in transactions:
            self.logger.info(str(transaction))

    def log_transactions_info(self, transactions: Iterable[Transaction]):
        self.log_profitable_transactions(transactions)
        self.log_unprofitable_transactions(transactions)
        self.log_worst_transaction(transactions)
        self.log_best_transaction(transactions)
