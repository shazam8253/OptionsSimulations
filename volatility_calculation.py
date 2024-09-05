import json
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

# Assuming you have the JSON data from the "btc_27sep24_chart_data.json" file
# Load the data from the JSON file
with open('btc_27sep24_chart_data.json', 'r') as f:
    data = json.load(f)

# Extract the ticks (timestamps) and close prices
timestamps = data['result']['ticks']
close_prices = data['result']['close']

# Convert timestamps to dates for easier interpretation
dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

# Calculate daily returns
daily_returns = np.log(np.array(close_prices[1:]) / np.array(close_prices[:-1]))

# Calculate annualized volatility
daily_volatility = np.std(daily_returns)
annualized_volatility = daily_volatility * np.sqrt(252)

print(f"Annualized Volatility: {annualized_volatility:.4f}")

# Plot the closing prices to visualize
plt.figure(figsize=(10, 6))
plt.plot(dates, close_prices, label='Closing Prices')
plt.title('BTC-27SEP24 Futures Closing Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# You can now use the calculated annualized_volatility in your option pricing model
