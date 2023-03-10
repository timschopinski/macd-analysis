from btc_data import get_data


def calculate_macd(n1: int = 12, n2: int = 26):
    data = get_data()[['close']].copy()
    data = data.head(1000)

    # Define a custom function to apply to each rolling window
    def calculate_ema(window):
        meter = 0
        denominator = 0
        n = len(window) - 1
        # print(n)
        alpha = 2 / (n + 1)
        # print(alpha)
        for index, p in enumerate(window[::-1]):
            meter += p * (1 - alpha) ** index
            denominator += (1 - alpha) ** index
            # print(f'meter: {meter}')
            # print(f'denominator: {denominator}')
            # print(f'p: {p}')
        ema = meter / denominator
        # print('*' * 40)
        # print('\n')
        # print(f'ema: {ema}')
        return ema

    # Use .rolling() to create a rolling window of size window_size, and .apply() to apply the custom function to each window
    data['ema1'] = data['close'].rolling(n1+1).apply(calculate_ema)
    data['ema2'] = data['close'].rolling(n2+1).apply(calculate_ema)
    data['macd'] = data['ema1'] - data['ema2']
    print(data)

    # remove Nan values
    data.dropna(subset=['macd'], inplace=True)

    # print('$' * 40)
    # print(data['ema1'])
    # print(data['ema2'])
    # print(data['macd'])

    for index, row in data.iterrows():
        # Get the close_sum value for the current row
        ema1 = row.loc['ema1']
        ema2 = row.loc['ema2']
        # print(f'ema1: {ema1}')
        # print(f'ema2: {ema2}')

    return data['macd']


if __name__ == '__main__':
    calculate_macd()
