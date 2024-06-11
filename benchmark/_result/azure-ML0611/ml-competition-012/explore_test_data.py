import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Check for missing values
missing_values = test_data.isnull().sum()

# Save the missing values information to a CSV file
missing_values.to_csv('/workspace/test_data_missing_values.csv')

# Get a summary of the data
summary = test_data.describe()

# Save the summary to a CSV file
summary.to_csv('/workspace/test_data_summary.csv')
