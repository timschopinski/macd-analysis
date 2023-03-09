import matplotlib.pyplot as plt
from btc_data import get_data

data = get_data()
data = data[['close']].copy()
data.plot(figsize=(12, 8), title="BTC/USD", fontsize=12)
plt.show()
print(data)
