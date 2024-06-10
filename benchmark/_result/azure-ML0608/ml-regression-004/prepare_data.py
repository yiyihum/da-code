import pandas as pd

# Load the datasets
historical_data = pd.read_csv('top_10000_1960-now.csv')
test_data = pd.read_csv('test.csv')

# Check for missing values in both datasets
print("Missing values in historical data:", historical_data.isnull().sum().sum())
print("Missing values in test data:", test_data.isnull().sum().sum())

# Display the first few rows of the historical data to understand the features better
print(historical_data.head())

# Display the first few rows of the test data to ensure it matches the structure of the historical data
print(test_data.head())
