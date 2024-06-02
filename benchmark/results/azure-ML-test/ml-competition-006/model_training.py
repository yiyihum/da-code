import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load the training data
train_data = pd.read_csv('train.csv')

# Split the data into features and target variable
X = train_data.drop(['Id', 'quality'], axis=1)
y = train_data['quality']

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Load the test data
test_data = pd.read_csv('test.csv')

# Make predictions on the test data
test_data['quality'] = model.predict(test_data.drop('Id', axis=1))

# Prepare the submission file
submission = test_data[['Id', 'quality']]

# Save the submission file
submission.to_csv('submission.csv', index=False)

print("Submission file created successfully.")
