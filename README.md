# MACD Analysis for BTC/USD
This analysis is based on the BTC/USD data.

## Overview
The MACD (Moving Average Convergence Divergence) is a popular technical analysis tool used to identify trends and momentum in financial markets. The MACD indicator is based on the difference between two Exponential Moving Averages (EMA), typically the 12-period EMA and the 26-period EMA.

## EMA Optimization
To optimize the MACD indicator, we will experiment with different values of the two EMAs. We will use a range of values for the two EMAs (between 5 and 35) and use the best values that result in the highest profit.

## Stop Loss
Stop loss is an important aspect of trading that helps limit losses in case of unexpected market movements. In this analysis, we will use a simple stop loss strategy where we exit the position if the price falls by a certain percentage (e.g. 2%).

## Backtesting
We will use the historical BTC/USD data to backtest our MACD strategy. We will simulate trading for a period of time and measure the profit/loss of the strategy. This will help us determine the effectiveness of the strategy.

## Results
The results of the MACD analysis are available in the main.ipynb notebook. The notebook contains the code for optimizing the MACD parameters, applying the stop loss strategy, and backtesting the strategy on the BTC/USD data.

## Source
The BTC/USD data used in this analysis is available on Kaggle at https://www.kaggle.com/datasets/prasoonkottarathil/btcinusd.

## Conclusion
The MACD indicator can be used to generate profitable trading signals in the BTC/USD market. By optimizing the EMAs and introducing a stop loss, the risk of the strategy can be minimized while still generating a satisfactory return on investment.

## License
MIT