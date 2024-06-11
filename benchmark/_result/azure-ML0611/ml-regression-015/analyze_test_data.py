import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Display basic information about the dataset
print(test_data.info())

# Display summary statistics
print(test_data.describe())

# Check for missing values
print(test_data.isnull().sum())
