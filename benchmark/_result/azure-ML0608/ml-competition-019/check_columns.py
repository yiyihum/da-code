import pandas as pd

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Print the column names for both train and test data
print("Train columns:", train_data.columns.tolist())
print("Test columns:", test_data.columns.tolist())
