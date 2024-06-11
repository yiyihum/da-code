import pandas as pd
import joblib

# Load the test essays data
test_essays = pd.read_csv('/workspace/test_essays.csv')

# Load the saved model and vectorizer
model = joblib.load('/workspace/llm_detection_model.pkl')
vectorizer = joblib.load('/workspace/llm_detection_vectorizer.pkl')

# Transform the test data using the loaded vectorizer
X_test_tfidf = vectorizer.transform(test_essays['text'])

# Predict probabilities on the test set
test_probabilities = model.predict_proba(X_test_tfidf)[:, 1]

# Create a submission DataFrame
submission = pd.DataFrame({
    'id': test_essays['id'],
    'generated': test_probabilities
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)

# Indicate success
print("Submission file saved successfully.")
