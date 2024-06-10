import pandas as pd
import numpy as np
import joblib

# Load the test data
test_data = pd.read_csv('/workspace/drugsComTest_raw.csv')

# Load the model and the tfidf vectorizer
regressor = joblib.load('/workspace/usefulness_linear_regressor.joblib')
tfidf = joblib.load('/workspace/tfidf_vectorizer.joblib')

# Preprocessing
# Clean the review text
test_data['clean_review'] = test_data['review'].str.replace(r"[^a-zA-Z\s]", "", regex=True).str.lower()

# Feature extraction from text
tfidf_matrix = tfidf.transform(test_data['clean_review'])

# Since the original model was trained with the rating feature, we need to include it
# Prepare the features for prediction
X_test = np.hstack((tfidf_matrix.toarray(), test_data[['rating']].values))

# Predict the 'usefulness' scores using the review text and rating
test_data['usefulness'] = regressor.predict(X_test)

# Save the predictions to a CSV file
test_data[['usefulness']].to_csv('/workspace/Usefulness.csv', index=False)
