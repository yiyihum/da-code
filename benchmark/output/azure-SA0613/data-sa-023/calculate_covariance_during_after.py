import pandas as pd

# Load the portfolio data
portfolio_df = pd.read_csv('/workspace/portfolio.csv', dtype={'Date': 'object'})
portfolio_df['Date'] = pd.to_datetime(portfolio_df['Date'], format='%d/%m/%Y')

# Define the epoch date ranges
during_epoch_start = pd.Timestamp('2007-01-01')
during_epoch_end = pd.Timestamp('2008-12-31')
after_epoch_start = pd.Timestamp('2009-01-01')
after_epoch_end = pd.Timestamp('2010-12-31')

# Filter data for the "during" and "after" epochs
during_df = portfolio_df[(portfolio_df['Date'] >= during_epoch_start) & (portfolio_df['Date'] <= during_epoch_end)]
after_df = portfolio_df[(portfolio_df['Date'] >= after_epoch_start) & (portfolio_df['Date'] <= after_epoch_end)]

# Calculate daily returns for each epoch
during_returns = during_df.drop(columns='Date').pct_change().dropna()
after_returns = after_df.drop(columns='Date').pct_change().dropna()

# Calculate the covariance matrices
during_cov_matrix = during_returns.cov()
after_cov_matrix = after_returns.cov()

# Load the template for the output format
template_df = pd.read_csv('/workspace/template.csv')

# Save the covariance matrices in the format provided by template.csv
during_cov_matrix.to_csv('/workspace/during_covariance.csv', index_label=template_df.columns[0], header=template_df.columns[1:])
after_cov_matrix.to_csv('/workspace/after_covariance.csv', index_label=template_df.columns[0], header=template_df.columns[1:])
