import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Display basic information about the dataset
print(test_data.info())

# Show the first few rows of the dataset
print(test_data.head())
