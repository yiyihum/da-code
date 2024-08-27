import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Drop the 'Unnamed: 0' and 'id' columns as they are not features
train_data.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)

# Convert categorical variables to dummy variables
train_data = pd.get_dummies(train_data, drop_first=True)

# Print the column names after transformation
print(train_data.columns.tolist())
