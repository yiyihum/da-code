import pandas as pd

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Display the last few columns of the dataframe to find the target variable
print(train_df.iloc[:, -10:].head())
