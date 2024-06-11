import pandas as pd
import joblib

# Load the trained model
model = joblib.load('emotion_classifier.joblib')

# Load and preprocess the test data
def load_test_data(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
    return [line.strip() for line in data]

test_data = load_test_data('test.txt')

# Make predictions on the test data
test_predictions = model.predict(test_data)

# Write the predictions to a CSV file
predictions_df = pd.DataFrame(test_predictions, columns=['emotion'])
predictions_df.to_csv('emotions.csv', index=False)
