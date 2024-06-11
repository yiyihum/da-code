import pandas as pd

# Load a subset of the training data
training_data_path = 'training.1600000.processed.noemoticon.csv'
training_columns = ['polarity', 'id', 'date', 'query', 'user', 'text']
nrows = 50000  # Load a subset of 50,000 rows
training_data = pd.read_csv(training_data_path, encoding='latin1', names=training_columns, nrows=nrows)

# Check the balance of classes
class_balance = training_data['polarity'].value_counts()
print(class_balance)
