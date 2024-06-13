import pandas as pd
import numpy as np



# Load the investment portfolio price data into the price variable.
prices = pd.read_csv("portfolio.csv")

# Convert the 'Date' column to a datetime index
prices['Date'] = pd.to_datetime(prices['Date'], format='%d/%m/%Y')
prices.set_index(['Date'], inplace = True)

# Import the CovarianceShrinkage object
from pypfopt.risk_models import CovarianceShrinkage

# Create the CovarianceShrinkage instance variable
cs = CovarianceShrinkage(prices)

# Compute the sample covariance matrix of returns
sample_cov = prices.pct_change().cov() * 252

# Compute the efficient covariance matrix of returns
e_cov = cs.ledoit_wolf()



# Display both the sample covariance_matrix and the efficient e_cov estimate
print("Sample Covariance Matrix\n", sample_cov, "\n")
print("Efficient Covariance Matrix\n", e_cov, "\n")


sample_cov.to_csv("sample_cov.csv")
e_cov.to_csv("e_cov.csv")