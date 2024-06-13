import pandas as pd
import numpy as np

# Load the historical quotes data
data = pd.read_csv('IBM - HistoricalQuotes.csv')

# Ensure the data is sorted by date
data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')
data.sort_values('date', inplace=True)

# Calculate daily returns
data['daily_return'] = data['close'].pct_change()

# Calculate the annualized volatility
# There are typically 252 trading days in a year
annualized_volatility = data['daily_return'].std() * np.sqrt(252)

# Output the annualized volatility
print(f"Annualized Volatility: {annualized_volatility}")

# Save the annualized volatility to a variable for later use
# (This will be used in the next step to calculate the Black-Scholes option prices)
annualized_volatility_var = annualized_volatility
