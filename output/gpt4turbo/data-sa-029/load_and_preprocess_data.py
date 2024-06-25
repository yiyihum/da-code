import pandas as pd

# Load the historical stock price data
# Specifying the date format to avoid the warning
data = pd.read_csv('IBM - HistoricalQuotes.csv', parse_dates=['date'], dayfirst=True)
data.set_index('date', inplace=True)

# Compute the daily percentage change in 'close' prices to get the returns
data['returns'] = data['close'].pct_change()

# Calculate the annualized standard deviation of the daily returns
annualized_volatility = data['returns'].std() * (252 ** 0.5)  # Assuming 252 trading days in a year

# Save the annualized volatility to a CSV file for later use
# Saving the value as a single value in a CSV file
with open('annualized_volatility.csv', 'w') as file:
    file.write(str(annualized_volatility))

print("Data loaded and preprocessed. Annualized volatility calculated.")
