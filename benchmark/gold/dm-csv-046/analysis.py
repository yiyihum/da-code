# Calculate the standard deviation of daily return of the stock

import numpy as np
import pandas as pd

StockPrices = pd.read_csv('MSFTPrices.csv')

StockPrices['Returns'] = StockPrices['Close'].pct_change()

print(StockPrices)
sigma_daily = np.std(StockPrices['Returns'])


# Annualize the standard deviation
sigma_annualized = sigma_daily*np.sqrt(252)
print(sigma_annualized)

# Calculate the annualized variance
variance_annualized = sigma_annualized**2
print(variance_annualized)