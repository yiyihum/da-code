import pandas as pd

# Load the test data
test_data = pd.read_csv('test.csv')

# Print the column names
print(test_data.columns.tolist())
