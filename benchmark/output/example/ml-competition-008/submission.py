import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# Load the train.csv and test.csv files into pandas dataframes
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

# Separate the features and the target variable in the training set
X_train = train_df.drop(['id', 'FloodProbability'], axis=1)
y_train = train_df['FloodProbability']

# Separate the id and the features in the test set
test_id = test_df['id']
X_test = test_df.drop('id', axis=1)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the probabilities on the test set
y_test_pred = model.predict(X_test)

# Create a dataframe for the submission
submission_df = pd.DataFrame({'id': test_id, 'FloodProbability': y_test_pred})

# Write the dataframe into the submission.csv file
submission_df.to_csv('submission.csv', index=False)
