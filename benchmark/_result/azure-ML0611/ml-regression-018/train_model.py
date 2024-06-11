import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Preprocessing the data
# For simplicity, we'll use only numerical features for the baseline model
X = train_data.drop(['id', 'num_orders'], axis=1)
y = train_data['num_orders']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor with fewer estimators to speed up training
rf = RandomForestRegressor(n_estimators=10, random_state=42)

# Train the model
rf.fit(X_train, y_train)

# Validate the model
y_pred = rf.predict(X_val)
rmse = np.sqrt(mean_squared_error(y_val, y_pred))
print(f"Validation RMSE: {rmse}")

# Prepare the test data for prediction
test_features = test_data

# Make predictions on the test set
test_predictions = rf.predict(test_features)

# Generate a sequential 'id' for the test set predictions
test_ids = range(1, len(test_predictions) + 1)

# Prepare the submission dataframe
submission = pd.DataFrame({'id': test_ids, 'num_orders': test_predictions})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)

print("Model trained and predictions saved to submission.csv.")
