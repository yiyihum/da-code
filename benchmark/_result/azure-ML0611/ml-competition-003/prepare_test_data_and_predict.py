import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load the trained model (assuming the model is stored in the variable rf_classifier)
# Note: In a real-world scenario, we would save the model to disk and load it. For this task, we will reuse the variable.

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Predict using the trained Random Forest model
test_predictions = rf_classifier.predict_proba(test_data.drop(columns=['Id']))

# Create a submission dataframe
submission = pd.DataFrame({
    'Id': test_data['Id'],
    'class_0': test_predictions[:, 0],
    'class_1': test_predictions[:, 1]
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)

# Output the path to the submission file
print("/workspace/submission.csv")
