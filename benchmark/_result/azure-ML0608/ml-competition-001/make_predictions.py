import pandas as pd
import joblib

# Load the trained model
clf = joblib.load('/workspace/churn_model.joblib')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Extract the customer IDs for the submission file
customer_ids = test_data['CustomerId']

# Add a dummy 'id' column to match the expected structure by the ColumnTransformer
test_data['id'] = 0

# Drop the 'CustomerId' and 'Surname' columns as they are not used in the model
X_test = test_data.drop(columns=['CustomerId', 'Surname'])

# Use the preprocessor from the trained pipeline to transform the test data
# This ensures that the test data undergoes the same preprocessing as the training data
preprocessor = clf.named_steps['preprocessor']
X_test_preprocessed = preprocessor.transform(X_test)

# Remove the dummy 'id' column before making predictions
X_test_preprocessed = X_test_preprocessed[:, 1:]

# Predict the probabilities of churn using the trained model
model = clf.named_steps['model']
test_preds = model.predict_proba(X_test_preprocessed)[:, 1]

# Create a submission dataframe
submission = pd.DataFrame({
    'id': customer_ids,
    'Exited': test_preds
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
