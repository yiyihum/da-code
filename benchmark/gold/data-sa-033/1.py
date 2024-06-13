
import pandas as pd
import numpy as np
from scipy.stats import genextreme



import pandas as pd

# Read the raw data into a Pandas DataFrame
data = pd.read_csv('GE - Historical.csv', parse_dates=['Date'])
data.set_index('Date', inplace=True)

# Calculate daily returns
losses = -data['Close'].pct_change().dropna()


# Compute the weekly block maxima for GE's stock
weekly_maxima = losses.resample("W").max()

# Fit the GEV distribution to the maxima
p = genextreme.fit(weekly_maxima)

# Compute the 99% VaR (needed for the CVaR computation)
VaR_99 = genextreme.ppf(0.99, *p)

# Compute the 99% CVaR estimate
CVaR_99 = (1 / (1 - 0.99)) * genextreme.expect(lambda x: x, 
           args=(p[0],), loc = p[1], scale = p[2], lb = VaR_99)

# Display the covering loss amount
print("Reserve amount: ", 1000000 * CVaR_99)