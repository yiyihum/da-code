from transformers import pipeline
import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the candidate labels
candidate_labels = ["business", "science and technology", "entertainment", "health"]

# Perform zero-shot classification on the first few titles
predictions = []
for title in test_df['TITLE'].head(5):
    result = classifier(title, candidate_labels)
    predictions.append(result['labels'][0])

# Add the predictions to the dataframe
test_df.loc[:4, 'CATEGORY'] = predictions

# Save the predictions to a CSV file
test_df.loc[:4, ['CATEGORY']].to_csv('/workspace/category.csv', index=False)
