import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Display data types of the columns
print(train_data.dtypes)
