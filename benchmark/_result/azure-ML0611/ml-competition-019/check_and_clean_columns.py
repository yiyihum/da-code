import pandas as pd

# Load the training and test datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Check the column names of the train and test datasets
print("Train dataset columns:", train_data.columns.tolist())
print("Test dataset columns:", test_data.columns.tolist())

# Drop the duplicate 'NObeyesdad' column from the train dataset if it exists
if 'NObeyesdad.1' in train_data.columns:
    train_data = train_data.drop(columns=['NObeyesdad.1'])

# Drop the 'NObeyesdad' column from the test dataset if it exists
if 'NObeyesdad' in test_data.columns:
    test_data = test_data.drop(columns=['NObeyesdad'])

# Save the cleaned datasets
train_data.to_csv('/workspace/clean_train.csv', index=False)
test_data.to_csv('/workspace/clean_test.csv', index=False)

# Display the first few rows of the cleaned train and test datasets
print(train_data.head())
print(test_data.head())
