import pandas as pd

# Load the train.csv and test.csv files into pandas dataframes
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

# Print the first few rows of the dataframes
print(train_df.head())
print(test_df.head())
