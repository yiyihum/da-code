import pandas as pd

# Load datasets
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# Print the data types of each column
print(train.dtypes)
print(test.dtypes)
