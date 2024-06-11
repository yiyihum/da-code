from transformers import pipeline
import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the candidate labels
candidate_labels = ["business", "science and technology", "entertainment", "health"]

# Perform zero-shot classification on a batch of titles
batch_size = 10  # Define a smaller batch size
predictions = []

for i in range(0, len(test_df), batch_size):
    batch_titles = test_df['TITLE'][i:i+batch_size].tolist()
    for title in batch_titles:
        result = classifier(title, candidate_labels)
        predictions.append(result['labels'][0])
        if len(predictions) % batch_size == 0:
            # Add the predictions to the dataframe
            test_df.loc[i:i+batch_size-1, 'CATEGORY'] = predictions[-batch_size:]
            # Save the predictions to a CSV file incrementally
            test_df[['CATEGORY']].to_csv('/workspace/category.csv', mode='a', header=not i, index=False)

# Check if there are any remaining predictions to save
if len(predictions) % batch_size != 0:
    test_df.loc[len(predictions)-len(predictions) % batch_size:, 'CATEGORY'] = predictions[-(len(predictions) % batch_size):]
    test_df[['CATEGORY']].to_csv('/workspace/category.csv', mode='a', header=False, index=False)
