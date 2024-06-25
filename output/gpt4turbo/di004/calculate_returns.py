import pandas as pd

# Load the stock data and benchmark data
stock_data = pd.read_csv('stock_data.csv')
benchmark_data = pd.read_csv('benchmark_data.csv')

# Merge the data on the 'Date' column
merged_data = pd.merge(stock_data, benchmark_data, on='Date')

# Drop rows with missing values
merged_data.dropna(inplace=True)

# Calculate daily returns for Amazon, Facebook, and S&P 500
merged_data['Amazon_Return'] = merged_data['Amazon'].pct_change()
merged_data['Facebook_Return'] = merged_data['Facebook'].pct_change()
merged_data['SP500_Return'] = merged_data['S&P 500'].pct_change()

# Drop the first row with NaN values after pct_change
merged_data.dropna(inplace=True)

# Calculate the average daily return differences
average_diff_amazon = (merged_data['Amazon_Return'] - merged_data['SP500_Return']).mean()
average_diff_facebook = (merged_data['Facebook_Return'] - merged_data['SP500_Return']).mean()

# Print the results
print(f"Average Daily Return Difference for Amazon: {average_diff_amazon}")
print(f"Average Daily Return Difference for Facebook: {average_diff_facebook}")
