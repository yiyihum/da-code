import pandas as pd

# Load the datasets
train_data_path = 'top_10000_1960-now.csv'
test_data_path = 'test.csv'

# Read the CSV files into Pandas DataFrames
train_df = pd.read_csv(train_data_path)
test_df = pd.read_csv(test_data_path)

# Display the first few rows of each DataFrame
print("Training Data:")
print(train_df.head())
print("\nTest Data:")
print(test_df.head())
