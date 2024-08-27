import pandas as pd

# Load the historical stock price data with explicit date format
data = pd.read_csv('IBM - HistoricalQuotes.csv', parse_dates=['date'], dayfirst=True, index_col='date')

# Sort the data by date in case it's not already sorted
data.sort_index(inplace=True)

# Save the preprocessed data to a new CSV file for further analysis
data.to_csv('preprocessed_ibm_data.csv')
