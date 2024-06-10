import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocess the data: Convert categorical data to numerical data
train_data = pd.get_dummies(train_data, columns=['country', 'store', 'product'])

# Split the data into features and target variable
X = train_data.drop(['id', 'num_sold', 'date'], axis=1)
y = train_data['num_sold']

# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=0)

# Define the model
model = RandomForestRegressor(n_estimators=100, random_state=0)

# Fit the model
model.fit(X_train, y_train)

# Predict on validation set
predictions = model.predict(X_valid)

# Calculate the mean absolute error of the predictions
mae = mean_absolute_error(y_valid, predictions)
print(f'Mean Absolute Error: {mae}')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Store the 'id' column to use later in the submission file
test_ids = test_data['id']

# Preprocess the test data
test_data = pd.get_dummies(test_data, columns=['country', 'store', 'product'])

# Ensure the test data has the same feature columns in the same order
test_data = test_data.reindex(columns=X.columns, fill_value=0)

# Make predictions on the test data
test_preds = model.predict(test_data)

# Save the predictions to a CSV file
output = pd.DataFrame({'id': test_ids, 'num_sold': test_preds})
output.to_csv('/workspace/submission.csv', index=False)
