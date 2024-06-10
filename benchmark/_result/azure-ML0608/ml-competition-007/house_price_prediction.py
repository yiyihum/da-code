import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the data
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Basic preprocessing
# For simplicity, we'll use only numerical features and fill missing values with the mean
numerical_features = train_data.select_dtypes(include=[np.number]).columns.tolist()
numerical_features.remove('SalePrice')  # Remove the target variable from the features list

# Calculate the mean only for numerical columns
numerical_means = train_data[numerical_features].mean()

X = train_data[numerical_features].fillna(numerical_means)
y = np.log(train_data['SalePrice'])  # Use the log-transform of the SalePrice as per competition evaluation metric

# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred_valid = model.predict(X_valid)
rmse = np.sqrt(mean_squared_error(y_valid, y_pred_valid))
print(f"Validation RMSE: {rmse}")

# Prepare the test data
X_test = test_data[numerical_features].fillna(numerical_means)
test_ids = test_data['Id']

# Make predictions on the test data
predictions = model.predict(X_test)

# Save the predictions in the submission format
submission = pd.DataFrame({'Id': test_ids, 'SalePrice': np.exp(predictions)})  # Exponentiate to reverse the log-transform
submission.to_csv('submission.csv', index=False)
print("Submission file created.")
