import joblib
import pandas as pd

# Load the trained model and the label encoder
rf_clf = joblib.load('/workspace/rf_clf.joblib')
label_encoder = joblib.load('/workspace/label_encoder.joblib')
X_test_vec = joblib.load('/workspace/X_test_vec.joblib')

# Load the original test dataset to add the predictions
test_df = pd.read_csv('/workspace/test.csv')

# Make predictions on the test set
test_predictions = rf_clf.predict(X_test_vec)
test_df['formatted_experience_level'] = label_encoder.inverse_transform(test_predictions)

# Save the predictions to a CSV file
test_df[['job_id', 'formatted_experience_level']].to_csv('/workspace/result.csv', index=False)
print('Predictions saved to result.csv')
