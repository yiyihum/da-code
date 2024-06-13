import pandas as pd
from sklearn.covariance import LedoitWolf

# Load the dataset
df = pd.read_csv('/workspace/portfolio.csv', index_col='Date')

# Calculate daily returns
returns = df.pct_change().dropna()

# Calculate the sample covariance matrix
sample_cov_matrix = returns.cov()

# Calculate the Ledoit-Wolf covariance matrix
lw = LedoitWolf()
lw_cov_matrix = lw.fit(returns).covariance_

# Save the sample covariance matrix using the template format
sample_cov_matrix.to_csv('/workspace/sample_covariance_matrix.csv')

# Save the Ledoit-Wolf covariance matrix using the template format
pd.DataFrame(lw_cov_matrix, index=returns.columns, columns=returns.columns).to_csv('/workspace/efficient_covariance_matrix.csv')
