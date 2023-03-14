from pandas import DataFrame


def get_macd_total_return(data: DataFrame, start_amount: float = 1000) -> float:
    holding = False
    capital = start_amount
    asset_amount = 0
    total_return = 0

    for i in range(len(data)):
        row = data.iloc[i]
        macd = row['macd']
        close_price = row['close']
        signal = row['signal']
        if macd > signal and not holding:
            asset_amount = capital / close_price
            capital = 0
            holding = True
        elif macd < signal and holding:
            capital = asset_amount * close_price
            asset_amount = 0
            holding = False
        if capital:
            total_return = capital - start_amount
        else:
            total_return = asset_amount * close_price - start_amount

    return total_return
