from models.transaction import TransactionType


class BuyAndSellLevelManager:
    def __init__(
        self,
        macd_buy_level: float | None = None,
        macd_sell_level: float | None = None,
    ):
        self.macd_buy_level = macd_buy_level
        self.macd_sell_level = macd_sell_level

    def check_level(self, macd_level: float, transaction_type: TransactionType) -> bool:
        if transaction_type == TransactionType.SELL:
            if macd_level > self.macd_sell_level:
                return True
        elif transaction_type == TransactionType.BUY:
            if macd_level < self.macd_buy_level:
                return True
        return False
