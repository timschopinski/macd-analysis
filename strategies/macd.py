from pandas import DataFrame
from datasets.btc_data import get_data
from backtesting.macd_backtester import MACDTester
from utils.time_frame import TimeFrame
import matplotlib.pyplot as plt


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


def get_macd_2(data: DataFrame, first_ema: int = 12, second_ema: int = 26) -> DataFrame:
    signal_length = 9

    def calculate_ema(window):
        meter = 0
        denominator = 0
        n = len(window) - 1
        alpha = 2 / (n + 1)

        for index, p in enumerate(window[::-1]):
            meter += p * (1 - alpha) ** index
            denominator += (1 - alpha) ** index
        ema = meter / denominator
        return ema

    data["ema1"] = data["close"].rolling(first_ema + 1).apply(calculate_ema)
    data["ema2"] = data["close"].rolling(second_ema + 1).apply(calculate_ema)
    data["macd"] = data["ema1"] - data["ema2"]
    data.dropna(subset=["macd"], inplace=True)
    data["signal"] = data["macd"].rolling(signal_length + 1).apply(calculate_ema)
    data.dropna(subset=["signal"], inplace=True)
    data["histogram"] = data["macd"] - data["signal"]
    return data


def get_macd(data: DataFrame, first_ema: int = 12, second_ema: int = 26) -> DataFrame:
    first_ema_data = data["close"].ewm(span=first_ema, adjust=False).mean()
    second_ema_data = data["close"].ewm(span=second_ema, adjust=False).mean()

    macd = first_ema_data - second_ema_data
    signal = macd.ewm(span=9, adjust=False).mean()

    data[f"ema{first_ema}"] = first_ema_data
    data[f"ema{second_ema}"] = second_ema_data
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
