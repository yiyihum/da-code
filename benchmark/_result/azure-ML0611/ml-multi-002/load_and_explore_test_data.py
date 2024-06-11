import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the dataframe
print(test_data.head())

# Check for any obvious indicators of new or used status
print("Unique values in 'Accidents or damage':", test_data['Accidents or damage'].unique())
print("Unique values in 'Clean title':", test_data['Clean title'].unique())
print("Unique values in '1-owner vehicle':", test_data['1-owner vehicle'].unique())
print("Unique values in 'Personal use only':", test_data['Personal use only'].unique())

# Check for missing values
print("\nMissing values in each column:")
print(test_data.isnull().sum())
