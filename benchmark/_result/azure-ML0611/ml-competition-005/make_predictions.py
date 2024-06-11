import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# We need to apply the same preprocessing to the test data as we did to the training data
# Predict probabilities on the test set
test_pred = clf.predict_proba(test_data.drop(['id'], axis=1))

# Create a DataFrame with the predictions
submission = pd.DataFrame(test_pred, columns=clf.classes_)

# Add the 'id' column from the test data
submission.insert(0, 'id', test_data['id'])

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)

# Display the first few lines of the submission file
print(submission.head())
