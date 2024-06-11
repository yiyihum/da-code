import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the TITLE column to understand the data better
print(test_df['TITLE'].head())
