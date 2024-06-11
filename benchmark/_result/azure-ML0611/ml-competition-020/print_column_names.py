import pandas as pd

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Print all column names
print(train_df.columns.tolist())
