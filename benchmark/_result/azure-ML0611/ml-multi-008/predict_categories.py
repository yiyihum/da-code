from transformers import pipeline
import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the candidate labels
candidate_labels = ["business", "science and technology", "entertainment", "health"]

# Perform zero-shot classification on the titles
predictions = []
for title in test_df['TITLE']:
    result = classifier(title, candidate_labels)
    predictions.append(result['labels'][0])

# Add the predictions to the dataframe
test_df['CATEGORY'] = predictions

# Correct the file path and save the predictions to a CSV file
test_df[['CATEGORY']].to_csv('category.csv', index=False)
