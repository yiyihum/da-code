import pandas as pd

# Load the training essays data
train_essays = pd.read_csv('/workspace/train_essays.csv')

# Display the first few rows of the dataframe
print(train_essays.head())

# Display the structure of the dataframe
print(train_essays.info())
