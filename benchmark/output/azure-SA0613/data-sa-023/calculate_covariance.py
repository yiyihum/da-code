import pandas as pd

# Load the portfolio data
portfolio_df = pd.read_csv('/workspace/portfolio.csv', dtype={'Date': 'object'})
portfolio_df['Date'] = pd.to_datetime(portfolio_df['Date'], format='%d/%m/%Y')

# Filter data for the "before" epoch (1-1-2005 to 31-12-2006)
before_epoch_start = pd.Timestamp('2005-01-01')
before_epoch_end = pd.Timestamp('2006-12-31')
before_df = portfolio_df[(portfolio_df['Date'] >= before_epoch_start) & (portfolio_df['Date'] <= before_epoch_end)]

# Calculate daily returns
before_returns = before_df.drop(columns='Date').pct_change().dropna()

# Calculate the covariance matrix
before_cov_matrix = before_returns.cov()

# Load the template for the output format
template_df = pd.read_csv('/workspace/template.csv')

# Save the covariance matrix in the format provided by template.csv
before_cov_matrix.to_csv('/workspace/before_covariance.csv', index_label=template_df.columns[0], header=template_df.columns[1:])
