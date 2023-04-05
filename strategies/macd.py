from pandas import DataFrame
from datasets.btc_data import get_data
from backtesting.macd_backtester import MACDTester
from utils.time_frame import TimeFrame
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_macd(macd: DataFrame, histogram: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(20, 8))
    ax.set_facecolor("lightgray")
    fig.set_facecolor("lightgray")
    plt.plot(macd["macd"], label="MACD", color="red", lw=0.4)
    plt.plot(macd["signal"], label="Signal", color="green", lw=0.3)
    if histogram:
        plt.bar(
            macd.index, macd["histogram"], color="orange", width=0.4, label="Histogram"
        )

    plt.axhline(0, color="black", lw=2)

    plt.xlabel("Date")
    plt.ylabel("MACD")
    plt.title("MACD and Signal with Histogram")
    plt.legend(loc="upper left")

    # display the plot
    plt.show()


def get_macd_3(
    data: pd.DataFrame, first_ema: int = 12, second_ema: int = 26
) -> pd.DataFrame:
    close = data["close"]
    alpha1 = 2 / (first_ema + 1)
    alpha2 = 2 / (second_ema + 1)

    ema1 = np.zeros(len(close))
    ema2 = np.zeros(len(close))

    ema1[0] = close[0]
    ema2[0] = close[0]

    for i in range(1, len(close)):
        ema1[i] = alpha1 * close[i] + (1 - alpha1) * ema1[i - 1]
        ema2[i] = alpha2 * close[i] + (1 - alpha2) * ema2[i - 1]

    macd = ema1 - ema2

    signal_alpha = 2 / (9 + 1)
    signal = np.zeros(len(close))
    signal[0] = macd[0]

    for i in range(1, len(close)):
        signal[i] = signal_alpha * macd[i] + (1 - signal_alpha) * signal[i - 1]

    histogram = macd - signal

    data[f"ema{first_ema}"] = pd.Series(ema1, index=data.index)
    data[f"ema{second_ema}"] = pd.Series(ema2, index=data.index)
    data["macd"] = pd.Series(macd, index=data.index)
    data["signal"] = pd.Series(signal, index=data.index)
    data["histogram"] = pd.Series(histogram, index=data.index)
    return data


def get_macd_2(data: DataFrame, first_ema: int = 12, second_ema: int = 26) -> DataFrame:
    signal_length = 9

    def calculate_ema(window):
        n = len(window)
        alpha = 2 / (n + 1)
        weights = (1 - alpha) ** np.arange(n)
        ema = window.dot(weights) / weights.sum()
        return ema

    data["ema1"] = (
        data["close"].rolling(first_ema, min_periods=first_ema).apply(calculate_ema)
    )
    data["ema2"] = (
        data["close"].rolling(second_ema, min_periods=second_ema).apply(calculate_ema)
    )
    data["macd"] = data["ema1"] - data["ema2"]
    data["signal"] = (
        data["macd"]
        .rolling(signal_length, min_periods=signal_length)
        .apply(calculate_ema)
    )
    data["histogram"] = data["macd"] - data["signal"]
    return data.dropna()


def get_macd(
    data: DataFrame,
    short_ema_length: int = 12,
    long_ema_length: int = 26,
    signal_length: int = 9,
) -> DataFrame:
    short_ema_data = data["close"].ewm(span=short_ema_length, adjust=False).mean()
    long_ema_data = data["close"].ewm(span=long_ema_length, adjust=False).mean()

    macd = short_ema_data - long_ema_data
    signal = macd.ewm(span=signal_length, adjust=False).mean()

    data[f"ema{short_ema_length}"] = short_ema_data
    data[f"ema{long_ema_length}"] = long_ema_data
    data["macd"] = macd
    data["signal"] = signal
    data["histogram"] = data["macd"] - data["signal"]
    return data


if __name__ == "__main__":
    data = get_data(TimeFrame.DAILY)
    macd_data = get_macd(data, 29, 48)
    # data = calculate_macd_data()
    print(macd_data)

    macd_tester = MACDTester(data)
    total_return = macd_tester.get_total_return()
    print(total_return)
    plot_macd(macd_data)
    macd_data = get_macd_2(data, 29, 48)
    # data = calculate_macd_data()
    print(macd_data)

    macd_tester = MACDTester(data)
    total_return = macd_tester.get_total_return()
    print(total_return)
    plot_macd(macd_data)

    macd_data = get_macd_3(data, 29, 48)
    print(macd_data)
    macd_tester = MACDTester(data)
    total_return = macd_tester.get_total_return()
    print(total_return)
    plot_macd(macd_data)
