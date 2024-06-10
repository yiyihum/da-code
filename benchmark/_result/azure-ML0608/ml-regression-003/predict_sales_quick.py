import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load the prepared datasets
train_prepared = pd.read_csv('/workspace/train_prepared.csv')
test_prepared = pd.read_csv('/workspace/test_prepared.csv')

# Separate features and target variable
X = train_prepared.drop(['Weekly_Sales', 'Date'], axis=1)  # Drop Date as it's not numeric
y = train_prepared['Weekly_Sales']

# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor with fewer trees to reduce computation time
rf_model = RandomForestRegressor(n_estimators=10, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Validate the model
y_pred = rf_model.predict(X_valid)
mae = mean_absolute_error(y_valid, y_pred)
print(f"Validation MAE: {mae}")

# Predict on the test set
test_prepared = test_prepared.drop('Date', axis=1)  # Drop Date as it's not numeric
test_predictions = rf_model.predict(test_prepared)

# Save the predictions to a CSV file
submission = pd.DataFrame({'Weekly_Sales': test_predictions})
submission.to_csv('/workspace/submission.csv', index=False)

# Output the first few rows of the submission file
print(submission.head())
