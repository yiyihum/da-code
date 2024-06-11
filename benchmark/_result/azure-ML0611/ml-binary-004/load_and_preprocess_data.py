import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Display basic information about the test data
print(test_data.info())
print(test_data.head())

# Check for missing values
print(test_data.isnull().sum())
