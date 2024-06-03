import pandas as pd

# Load the datasets
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
syn_crab_data = pd.read_csv('syn_crab_data.csv')

# Print the first few rows of each dataset
print(train.head())
print(test.head())
print(syn_crab_data.head())
