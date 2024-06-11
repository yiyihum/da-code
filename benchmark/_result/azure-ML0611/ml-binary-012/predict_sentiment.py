import pandas as pd
import joblib

# Load the test data
test_data_path = 'testdata.manual.2009.06.14.csv'
test_columns = ['id', 'date', 'query', 'user', 'text']
test_data = pd.read_csv(test_data_path, encoding='latin1', names=test_columns)

# Preprocess the text data: remove URLs, mentions, and non-alphabetic characters
test_data['text_clean'] = test_data['text'].str.replace(r'http\S+', '', regex=True)
test_data['text_clean'] = test_data['text_clean'].str.replace(r'@\w+', '', regex=True)
test_data['text_clean'] = test_data['text_clean'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
test_data['text_clean'] = test_data['text_clean'].str.lower().str.strip()

# Load the trained model
model = joblib.load('sentiment_model.joblib')

# Predict the sentiment of the test data
test_data['emotion'] = model.predict(test_data['text_clean'])

# Save the predictions to a CSV file
prediction_output_path = 'sentiment.csv'
test_data[['emotion']].to_csv(prediction_output_path, index=False)

print(f'Predictions saved to {prediction_output_path}')
