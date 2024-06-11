import pandas as pd

# Load the datasets
train_data = pd.read_csv('/workspace/New_York_cars.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the train and test datasets
print(train_data.head())
print(test_data.head())
