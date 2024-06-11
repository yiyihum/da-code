import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

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
