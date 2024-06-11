import pandas as pd

# Load the datasets
train_df = pd.read_csv('/workspace/bodyPerformance.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Check for missing values in the training data
train_missing_values = train_df.isnull().sum()

# Check for missing values in the test data
test_missing_values = test_df.isnull().sum()

# Output the missing values information
print("Training Data Missing Values:\n", train_missing_values)
print("\nTest Data Missing Values:\n", test_missing_values)
