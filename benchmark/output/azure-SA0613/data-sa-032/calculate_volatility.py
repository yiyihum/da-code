import pandas as pd

# Load the dataset
df = pd.read_csv('crisis_portfolio.csv', parse_dates=['Date'], dayfirst=True)

# Calculate daily returns
df_returns = df.set_index('Date').pct_change().dropna()

# Calculate equal weights for the portfolios
num_stocks = len(df_returns.columns)
weights_with_citi = [1 / num_stocks] * num_stocks
# Assuming 'Citibank' is the first column, we exclude it for the without Citi portfolio
weights_without_citi = [1 / (num_stocks - 1)] * (num_stocks - 1)

# Calculate portfolio returns with Citibank
df_returns['Portfolio With Citi'] = (df_returns * weights_with_citi).sum(axis=1)

# Calculate portfolio returns without Citibank
# Dropping the 'Citibank' column by name to ensure it is excluded
df_returns_without_citi = df_returns.drop(columns=['Citibank'])
df_returns['Portfolio Without Citi'] = (df_returns_without_citi * weights_without_citi).sum(axis=1)

# Calculate 30-day rolling window volatility (standard deviation of returns)
df_volatility_with_citi = df_returns['Portfolio With Citi'].rolling(window=30).std()
df_volatility_without_citi = df_returns['Portfolio Without Citi'].rolling(window=30).std()

# Combine the volatilities into a single DataFrame
df_volatility = pd.DataFrame({
    'Date': df_returns.index,
    'With Citi': df_volatility_with_citi,
    'Without Citi': df_volatility_without_citi
})

# Save the results to result.csv
df_volatility.to_csv('result.csv', index=False, date_format='%d/%m/%Y')
