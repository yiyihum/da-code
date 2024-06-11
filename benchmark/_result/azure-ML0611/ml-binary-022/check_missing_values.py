import pandas as pd

# Load the datasets
data = pd.read_csv('/workspace/data.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Check for missing values in the training data
missing_values_train = data.isnull().sum().sum()
print(f"Missing values in training data: {missing_values_train}")

# Check for missing values in the test data
missing_values_test = test_data.isnull().sum().sum()
print(f"Missing values in test data: {missing_values_test}")
