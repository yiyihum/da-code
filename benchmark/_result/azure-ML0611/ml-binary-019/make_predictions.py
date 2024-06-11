import pandas as pd
import joblib

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Load the trained model and label encoders
model = joblib.load('/workspace/mushroom_classifier.joblib')
label_encoders = {}
for column in test_data.columns:
    label_encoders[column] = joblib.load(f'/workspace/{column}_encoder.joblib')
    test_data[column] = label_encoders[column].transform(test_data[column])

# Make predictions on the test data
predictions = model.predict(test_data)

# Map the numerical predictions back to the original labels
inverse_label_map = {0: 'e', 1: 'p'}
predictions = [inverse_label_map[pred] for pred in predictions]

# Save the predictions to a CSV file
prediction_df = pd.DataFrame(predictions, columns=['class'])
prediction_df.to_csv('/workspace/class.csv', index=False)
