import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X_train = train_data.drop(columns=['id', 'FloodProbability'])
y_train = train_data['FloodProbability']

# Initialize the Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Prepare test data features
X_test = test_data.drop(columns=['id'])

# Predict the FloodProbability for the test data
test_predictions = model.predict(X_test)

# Create a submission dataframe
submission = pd.DataFrame({
    'id': test_data['id'],
    'FloodProbability': test_predictions
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
