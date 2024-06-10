import pandas as pd
import joblib

# Load the trained model
model = joblib.load('/workspace/emotion_classifier.joblib')

# Load the test data, assuming each line is a separate document
with open('/workspace/test.txt', 'r') as file:
    test_data = pd.DataFrame(file.readlines(), columns=['text'])
test_data['text'] = test_data['text'].str.strip()  # Remove any trailing newline characters

# Predict the emotions
test_data['emotion'] = model.predict(test_data['text'])

# Save the predictions to a CSV file
test_data[['emotion']].to_csv('/workspace/emotions.csv', index=False)
