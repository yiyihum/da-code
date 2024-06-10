import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Display basic information about the training data
print(train_data.info())
print(train_data.head())

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Display basic information about the test data
print(test_data.info())
print(test_data.head())
