import pandas as pd

# Load the training and test datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display basic information about the datasets
print("Training Data Info:")
print(train_data.info())
print("\nTest Data Info:")
print(test_data.info())

# Display the first few rows of the training data
print("\nTraining Data Head:")
print(train_data.head())

# Display the first few rows of the test data
print("\nTest Data Head:")
print(test_data.head())
