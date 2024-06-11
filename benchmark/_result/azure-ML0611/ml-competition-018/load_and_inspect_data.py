import pandas as pd

# Load the test essays data
test_essays = pd.read_csv('/workspace/test_essays.csv')

# Display the first few rows of the dataframe
print(test_essays.head())

# Display the structure of the dataframe
print(test_essays.info())
