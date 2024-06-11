import pandas as pd
import joblib

# Load the test dataset
test_data = pd.read_csv('/workspace/activity_test.csv')

# Load the trained Random Forest classifier
rf_classifier = joblib.load('/workspace/rf_classifier.joblib')

# Make predictions on the test dataset
test_predictions = rf_classifier.predict(test_data)

# Save the predictions to a CSV file
prediction_df = pd.DataFrame(test_predictions, columns=['Activity'])
prediction_df.to_csv('/workspace/activity.csv', index=False)

print("Predictions saved to activity.csv.")
