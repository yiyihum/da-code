import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Load datasets
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# One-hot encode the 'EJ' column
encoder = OneHotEncoder()
train_EJ_encoded = pd.DataFrame(encoder.fit_transform(train[['EJ']]).toarray())
test_EJ_encoded = pd.DataFrame(encoder.transform(test[['EJ']]).toarray())

# Add the encoded 'EJ' column back to the datasets
train = pd.concat([train, train_EJ_encoded], axis=1)
test = pd.concat([test, test_EJ_encoded], axis=1)

# Drop the original 'EJ' column
train = train.drop('EJ', axis=1)
test = test.drop('EJ', axis=1)

# Print the data types of each column
print(train.dtypes)
print(test.dtypes)
