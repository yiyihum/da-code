import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Display basic information about the dataset
info = test_data.info()

# Check for missing values
missing_values = test_data.isnull().sum()

# Output the information and missing values to text files
info.to_csv('/workspace/test_data_info.txt', index=False)
missing_values.to_csv('/workspace/test_data_missing_values.csv', index=False)
