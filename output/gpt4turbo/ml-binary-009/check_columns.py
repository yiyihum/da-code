import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Print the column names
print(train_data.columns.tolist())