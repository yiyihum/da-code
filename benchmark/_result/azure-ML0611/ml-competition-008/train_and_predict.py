import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X = train_data.drop(columns=['id', 'FloodProbability'])
y = train_data['FloodProbability']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the XGBoost regressor
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

# Fit the model to the training data
model.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Keep the 'id' column to use in the submission file
test_ids = test_data['id']

# Drop the 'id' column as it's not a feature for prediction
X_test = test_data.drop(columns=['id'])

# Use the trained model to predict the 'FloodProbability' on the test set
test_predictions = model.predict(X_test)

# Create a submission DataFrame
submission = pd.DataFrame({
    'id': test_ids,
    'FloodProbability': test_predictions
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)

# Display the first few lines of the submission file
print(submission.head())
