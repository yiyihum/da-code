import pandas as pd

# Load the datasets
training_data = pd.read_csv('twitter_training.csv')
validation_data = pd.read_csv('twitter_validation.csv')

# Display the first few rows of the training data
print(training_data.head())

# Display the first few rows of the validation data
print(validation_data.head())

# Check for unique sentiment labels in the training data
print('Unique sentiment labels in training data:', training_data['label'].unique())
