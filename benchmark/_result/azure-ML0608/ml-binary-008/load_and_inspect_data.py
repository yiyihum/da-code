import pandas as pd

# Load the training data
train_data = pd.read_csv('train_u6lujuX_CVtuZ9i.csv')

# Display the first few rows of the training data
print(train_data.head())

# Load the test data
test_data = pd.read_csv('test.csv')

# Display the first few rows of the test data
print(test_data.head())
