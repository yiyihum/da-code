import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/Clean_Dataset.csv')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the training and test data
print(train_data.head())
print(test_data.head())
