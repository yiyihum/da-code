import pandas as pd

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Display basic information about the dataset
info = train_df.info()

# Display statistical summary of the dataset
description = train_df.describe()

# Check for missing values
missing_values = train_df.isnull().sum()

# Save the EDA results to a text file
with open('/workspace/eda_results.txt', 'w') as f:
    f.write("Dataset Info:\n")
    f.write(str(info) + "\n\n")
    f.write("Statistical Summary:\n")
    f.write(str(description) + "\n\n")
    f.write("Missing Values:\n")
    f.write(str(missing_values) + "\n")

print("EDA results saved to eda_results.txt")
