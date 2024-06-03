import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error
from preprocess_data import preprocess_data

# Load the train and test data
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Preprocess the data
train_data, test_data = preprocess_data(train_data, test_data)

# Split the train data into features and target variable
X = train_data.drop('microbusiness_density', axis=1)
y = train_data['microbusiness_density']

# Train a SGDRegressor model
model = SGDRegressor(max_iter=1000, tol=1e-3)
model.fit(X, y)

# Save the 'row_id' column for the submission file and then drop it from the test data
row_id = test_data['row_id']
test_data = test_data.drop('row_id', axis=1)

# Make predictions on the test data
test_predictions = model.predict(test_data)

# Write the predictions into a submission file
submission = pd.DataFrame({'row_id': row_id, 'microbusiness_density': test_predictions})
submission.to_csv('submission.csv', index=False)

# Calculate the root mean squared error on the train data for reference
train_predictions = model.predict(X)
rmse = mean_squared_error(y, train_predictions, squared=False)
print(f'Train RMSE: {rmse}')
