import pandas as pd

# Load the test dataset
test_df = pd.read_csv('/workspace/test.csv')

# Display basic information about the dataset
print(test_df.info())

# Display summary statistics for numerical features
print(test_df.describe())

# Check for missing values
print(test_df.isnull().sum())
