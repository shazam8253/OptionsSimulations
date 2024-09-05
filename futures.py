import datetime
import json
import time

import matplotlib.pyplot as plt
import requests

# Deribit API endpoint for historical trades
api_url = "https://test.deribit.com/api/v2/public/get_tradingview_chart_data"

# Instrument name for the selected futures contract
instrument_name = "BTC-27SEP24"

# Date range: The last 30 days
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=30)
print(f"Start Date: {start_date}, End Date: {end_date}")

# Convert dates to UNIX timestamps in milliseconds
end_timestamp = int(time.mktime(end_date.timetuple()) * 1000)
start_timestamp = int(time.mktime(start_date.timetuple()) * 1000)
print(f"Start Timestamp: {start_timestamp}, End Timestamp: {end_timestamp}")

# Parameters for the API request
params = {
    "instrument_name": instrument_name,
    "start_timestamp": start_timestamp,
    "end_timestamp": end_timestamp,
    "resolution": "1D"
}

# Initialize an empty list to store all trades
# Send the request to the Deribit API
response = requests.get(api_url, params=params)
data = response.json()

with open('btc_27sep24_chart_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Extract data from the response
timestamps = [datetime.datetime.fromtimestamp(ts / 1000) for ts in data['result']['ticks']]
open_prices = data['result']['open']
high_prices = data['result']['high']
low_prices = data['result']['low']
close_prices = data['result']['close']
volumes = data['result']['volume']

# Plot the data: closing prices and volumes
plt.figure(figsize=(10, 6))
plt.plot(timestamps, close_prices, label='Closing Prices', color='blue')
plt.bar(timestamps, volumes, alpha=0.3, label='Volume', color='orange')

# Add labels and title
plt.title('BTC-27SEP24 Futures Closing Prices and Volume Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
