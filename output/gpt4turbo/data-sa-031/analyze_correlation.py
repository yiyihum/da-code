import pandas as pd

# Load the datasets with the correct date format
portfolio_df = pd.read_csv('crisis_portfolio.csv', parse_dates=['Date'], dayfirst=True)
delinquency_df = pd.read_csv('mortgage_delinquency.csv', parse_dates=['Date'])

# Merge the datasets on the Date column
merged_df = pd.merge(portfolio_df, delinquency_df, on='Date', how='inner')

# Calculate the average portfolio return
merged_df['Average Portfolio Return'] = merged_df[['Citibank', 'Morgan Stanley', 'Goldman Sachs', 'J.P. Morgan']].mean(axis=1)

# Split the data into pre-crisis and post-crisis
pre_crisis_data = merged_df[merged_df['Date'] < pd.to_datetime('2008-01-01')]
post_crisis_data = merged_df[merged_df['Date'] >= pd.to_datetime('2008-01-01')]

# Calculate the correlation before and after the crisis
pre_crisis_corr = pre_crisis_data['Average Portfolio Return'].corr(pre_crisis_data['Mortgage Delinquency Rate'])
post_crisis_corr = post_crisis_data['Average Portfolio Return'].corr(post_crisis_data['Mortgage Delinquency Rate'])

# Save the results to a CSV file
results = pd.DataFrame({
    'Period': ['Pre-Crisis', 'Post-Crisis'],
    'Correlation': [pre_crisis_corr, post_crisis_corr]
})
results.to_csv('result.csv', index=False)
