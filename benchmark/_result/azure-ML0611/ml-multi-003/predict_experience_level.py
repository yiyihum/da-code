import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Load the training data
df = pd.read_csv('/workspace/postings.csv')

# Preprocessing and feature extraction
df['description'] = df['description'].fillna('')  # Fill NaN descriptions with empty string
X = df['description']
y = df['formatted_experience_level']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with TF-IDF Vectorizer and Multinomial Naive Bayes Classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=1000)),
    ('clf', MultinomialNB())
])

# Train the model
pipeline.fit(X_train, y_train)

# Validate the model
y_pred = pipeline.predict(X_val)
print(classification_report(y_val, y_pred))

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')
test_df['description'] = test_df['description'].fillna('')  # Fill NaN descriptions with empty string
X_test = test_df['description']

# Predict the experience level for the test data
test_df['formatted_experience_level'] = pipeline.predict(X_test)

# Save the results to result.csv
test_df[['job_id', 'formatted_experience_level']].to_csv('/workspace/result.csv', index=False)
