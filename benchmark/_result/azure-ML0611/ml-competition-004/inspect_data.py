import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Print the column names to identify any unexpected columns
print("Training data columns:", train_data.columns.tolist())
