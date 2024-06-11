import pandas as pd

# Load the trained classifier
clf = pd.read_pickle('model.pkl')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Keep the CustomerID for the output file
customer_ids = test_data['CustomerID']

# Drop the CustomerID from the test data as it's not a feature
X_test = test_data.drop('CustomerID', axis=1)

# Preprocessing of test data and prediction
predictions = clf.predict(X_test)

# Create a DataFrame with the CustomerID and the predictions
output = pd.DataFrame({'CustomerID': customer_ids, 'Churn': predictions})

# Save the predictions to a CSV file
output.to_csv('/workspace/churn.csv', index=False)
