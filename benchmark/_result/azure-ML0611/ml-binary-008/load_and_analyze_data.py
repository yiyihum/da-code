import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train_u6lujuX_CVtuZ9i.csv')

# Display the first few rows of the dataframe
print(train_data.head())

# Display the summary of the dataframe
print(train_data.info())

# Display the summary statistics of the dataframe
print(train_data.describe(include='all'))

# Check for missing values
print(train_data.isnull().sum())
