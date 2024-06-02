import pandas as pd

# Load datasets
train = pd.read_csv('train.csv')

# Print the unique values of 'EJ'
print(train['EJ'].unique())
