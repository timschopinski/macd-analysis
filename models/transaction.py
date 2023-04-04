from enum import Enum
from typing import NamedTuple
from pandas import Timestamp


class TransactionType(Enum):
    BUY = "BUY"
    SELL = "SELL"

    def __str__(self):
        return self.value


class Transaction(NamedTuple):
    """
    This class represents a Transaction
    with a date as x value and price as y value
    """

    date: Timestamp
    price: float
    amount: float
    profit: float
    type: TransactionType

    def __str__(self):
        return f"""
        Transaction(Type: {self.type},
        Date: {self.date},
        Price: {self.price},
        Profit: {self.profit},
        Amount: {self.amount}
        """
