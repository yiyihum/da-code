import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load the training data and test data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Separate features and target variable from the training data
X_train = train_data.drop(columns=['id', 'Hardness'])
y_train = train_data['Hardness']

# Features from the test data
X_test = test_data.drop(columns=['id'])

# Initialize and train the Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)

# Make predictions on the test set
test_data['Hardness'] = rf_regressor.predict(X_test)

# Prepare the submission file
submission = test_data[['id', 'Hardness']]
submission.to_csv('/workspace/submission.csv', index=False)
print(submission.head())
