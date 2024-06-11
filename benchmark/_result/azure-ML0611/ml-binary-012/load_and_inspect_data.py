import pandas as pd

# Load the training data
training_data_path = 'training.1600000.processed.noemoticon.csv'
training_columns = ['polarity', 'id', 'date', 'query', 'user', 'text']
training_data = pd.read_csv(training_data_path, encoding='latin1', names=training_columns)

# Display the first few rows of the training data
print(training_data.head())

# Load the test data
test_data_path = 'testdata.manual.2009.06.14.csv'
test_columns = ['id', 'date', 'query', 'user', 'text']
test_data = pd.read_csv(test_data_path, encoding='latin1', names=test_columns)

# Display the first few rows of the test data
print(test_data.head())
