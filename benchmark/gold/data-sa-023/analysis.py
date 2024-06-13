import pandas as pd
import numpy as np

# Load the investment portfolio price data into the price variable.
prices = pd.read_csv("portfolio.csv")

# Convert the 'Date' column to a datetime index
prices['Date'] = pd.to_datetime(prices['Date'], format='%d/%m/%Y')
prices.set_index(['Date'], inplace=True)

# Import the CovarianceShrinkage object
from pypfopt.risk_models import CovarianceShrinkage

# Create a dictionary of time periods (or 'epochs')
epochs = {
    'before': {'start': '1-1-2005', 'end': '31-12-2006'},
    'during': {'start': '1-1-2007', 'end': '31-12-2008'},
    'after': {'start': '1-1-2009', 'end': '31-12-2010'}
}

# Compute the efficient covariance for each epoch and save to CSV
e_cov = {}
for epoch in epochs.keys():
    sub_price = prices.loc[epochs[epoch]['start']:epochs[epoch]['end']]
    e_cov[epoch] = CovarianceShrinkage(sub_price).ledoit_wolf()
    e_cov[epoch].to_csv(f"{epoch}_covariance.csv")

