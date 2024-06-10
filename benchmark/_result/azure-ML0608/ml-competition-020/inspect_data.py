import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Display the first few rows of the training data and the column names
print(train_data.head())
print(train_data.columns.tolist())
