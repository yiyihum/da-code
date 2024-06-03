import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the training data
train_data = pd.read_csv('train.csv')
X_train = train_data.drop(['id', 'Hardness'], axis=1)
y_train = train_data['Hardness']

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('test.csv')
X_test = test_data.drop(['id'], axis=1)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Create a DataFrame for the submission
submission = pd.DataFrame({
    'id': test_data['id'],
    'Hardness': y_pred
})

# Write the submission DataFrame to a CSV file
submission.to_csv('submission.csv', index=False)
