from pandas import DataFrame


def backtest_macd(data: DataFrame, start_amount: float = 1000) -> float:
    holding = False
    capital = start_amount
    asset_amount = 0
    close_price = 0
    for i in range(len(data)):
        row = data.iloc[i]
        histogram = row['histogram']
        close_price = row['close']
        if histogram > 0 and not holding:
            asset_amount = capital / close_price
            capital = 0
            holding = True
        elif histogram < 0 and holding:
            capital = asset_amount * close_price
            asset_amount = 0
            holding = False

    if capital:
        total_return = capital - start_amount
    else:
        total_return = asset_amount * close_price - start_amount

    return total_return
