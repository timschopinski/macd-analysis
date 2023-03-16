from enum import Enum


class StopLossOrder(Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    HOLD = 'HOLD'

    def __str__(self):
        return self.value
