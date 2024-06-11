import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Display basic information about the dataset
print(train_data.info())

# Display summary statistics for numerical features
print(train_data.describe())

# Check for missing values
missing_values = train_data.isnull().sum()
print(missing_values)

# Save the missing values to a text file for reference
missing_values.to_csv('/workspace/data_missing_values.txt', index=True)

# Preprocessing steps will be added here in the next iteration
