import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import median_absolute_error

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate the features and target
X_train = train_data.drop(columns=['id', 'Hardness'])
y_train = train_data['Hardness']

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')
X_test = test_data.drop(columns=['id'])

# Initialize the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)

# Create the submission dataframe
submission = pd.DataFrame({
    'id': test_data['id'],
    'Hardness': predictions
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
