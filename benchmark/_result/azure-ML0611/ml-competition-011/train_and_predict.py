import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load the datasets
train_df = pd.read_csv('/workspace/train.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Split the training data into features and target
X_train = train_df.drop(['id', 'yield'], axis=1)
y_train = train_df['yield']

# Initialize a Random Forest Regressor as a baseline model
rf = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf.fit(X_train, y_train)

# Prepare the test features
X_test = test_df.drop(['id'], axis=1)

# Use the trained Random Forest model to make predictions on the test set
test_predictions = rf.predict(X_test)

# Create a submission DataFrame
submission_df = pd.DataFrame({
    'id': test_df['id'],
    'yield': test_predictions
})

# Save the submission file
submission_df.to_csv('/workspace/submission.csv', index=False)

print("Submission file created.")
