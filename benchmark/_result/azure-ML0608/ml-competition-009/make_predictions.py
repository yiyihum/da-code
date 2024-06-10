import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load the training and test data
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Preprocess the data: convert 'Sex' from categorical to numerical
train_data['Sex'] = train_data['Sex'].map({'M': 0, 'F': 1, 'I': 2})
test_data['Sex'] = test_data['Sex'].map({'M': 0, 'F': 1, 'I': 2})

# Separate features and target from the training data
X_train = train_data.drop(['id', 'Rings'], axis=1)
y_train = train_data['Rings']

# Prepare the test data, preserving the 'id' column for the submission file
test_ids = test_data['id']
X_test = test_data.drop('id', axis=1)

# Initialize and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test data
predictions = model.predict(X_test)

# Create the submission DataFrame
submission = pd.DataFrame({
    'id': test_ids,
    'Rings': predictions
})

# Round the predictions to the nearest integer as Rings is an integer in the training set
submission['Rings'] = submission['Rings'].round().astype(int)

# Save the submission file
submission.to_csv('submission.csv', index=False)
