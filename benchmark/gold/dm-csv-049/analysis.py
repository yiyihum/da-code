# Calculate the standard deviation of daily return of the stock

import numpy as np
import pandas as pd

StockPrices = pd.read_csv('MSFTPrices.csv')

StockPrices['Returns'] = StockPrices['Close'].pct_change()

sigma_daily = np.std(StockPrices['Returns'])

# Import skew from scipy.stats
from scipy.stats import skew

# Drop the missing values
clean_returns = StockPrices['Returns'].dropna()

# Calculate the third moment (skewness) of the returns distribution
returns_skewness = skew(clean_returns)
print(returns_skewness)
# Import kurtosis from scipy.stats
from scipy.stats import kurtosis

# Calculate the excess kurtosis of the returns distribution
excess_kurtosis = kurtosis(clean_returns)

# Derive the true fourth moment of the returns distribution
fourth_moment = excess_kurtosis + 3
print(fourth_moment)

# # Import shapiro from scipy.stats
# from scipy.stats import shapiro

# # Run the Shapiro-Wilk test on the stock returns
# shapiro_results = shapiro(clean_returns)
# print("Shapiro results:", shapiro_results)

# # Extract the p-value from the shapiro_results
# p_value = shapiro_results[1]
# print("P-value: ", p_value)