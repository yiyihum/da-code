import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Check for missing values
missing_values = test_data.isnull().sum()

# Output the missing values to a text file
missing_values.to_csv('/workspace/missing_values.txt', header=True)
