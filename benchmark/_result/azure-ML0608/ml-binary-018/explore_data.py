import pandas as pd

# Load the training dataset
train_data = pd.read_csv('/workspace/healthcare-dataset-stroke-data.csv')

# Display basic information about the dataset
print(train_data.info())
print(train_data.head())
