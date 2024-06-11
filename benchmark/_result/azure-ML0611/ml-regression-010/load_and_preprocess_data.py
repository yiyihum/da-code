import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/drugsComTrain_raw.csv')

# Display basic information about the dataset
print(train_data.info())
print(train_data.head())

# Check for any missing values
print(train_data.isnull().sum())
