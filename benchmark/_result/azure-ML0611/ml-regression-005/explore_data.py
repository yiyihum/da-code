import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Display basic information about the dataset
info = train_data.info()

# Display summary statistics for numerical features
description = train_data.describe()

# Check for missing values
missing_values = train_data.isnull().sum()

# Save the exploration results to text files
info.to_csv('/workspace/data_info.txt', index=False)
description.to_csv('/workspace/data_description.txt', index=False)
missing_values.to_csv('/workspace/data_missing_values.txt', index=False)

print("Data exploration results saved.")
