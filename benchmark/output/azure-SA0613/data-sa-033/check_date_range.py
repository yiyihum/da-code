import pandas as pd

# Load the historical stock data
data = pd.read_csv('/workspace/GE - Historical.csv')

# Convert the Date column to datetime type
data['Date'] = pd.to_datetime(data['Date'])

# Check the date range of the dataset
date_range = (data['Date'].min(), data['Date'].max())
print(f"Date range of the dataset: {date_range}")
