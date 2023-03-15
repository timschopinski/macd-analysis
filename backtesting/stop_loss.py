from enum import Enum


class StopLossOrder(Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    HOLD = 'HOLD'

    def __str__(self):
        return self.value


class StopLossManager:

    def __init__(self, stop_loss: float):
        self._stop_loss = stop_loss
        self._recent_action_price = 0

    def set_recent_action_price(self, price: float) -> None:
        self._recent_action_price = price

    def get_order(self, price: float, holding: bool):
        if self._stop_loss is None:
            return StopLossOrder.HOLD
        if holding and self._recent_action_price / price - 1 > self._stop_loss:
            return StopLossOrder.SELL
