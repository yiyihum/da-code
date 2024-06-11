import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Load a balanced subset of the training data
training_data_path = 'training.1600000.processed.noemoticon.csv'
training_columns = ['polarity', 'id', 'date', 'query', 'user', 'text']
nrows = 25000  # Load 25,000 rows of each class
skiprows = 1 + nrows  # Skip the first 25,000 negative rows

# Load 25,000 negative and 25,000 positive samples to ensure balance
negative_data = pd.read_csv(training_data_path, encoding='latin1', names=training_columns, nrows=nrows)
positive_data = pd.read_csv(training_data_path, encoding='latin1', names=training_columns, nrows=nrows, skiprows=skiprows)

# Combine negative and positive data
balanced_data = pd.concat([negative_data, positive_data])

# Preprocess the text data: remove URLs, mentions, and non-alphabetic characters
balanced_data['text_clean'] = balanced_data['text'].str.replace(r'http\S+', '', regex=True)
balanced_data['text_clean'] = balanced_data['text_clean'].str.replace(r'@\w+', '', regex=True)
balanced_data['text_clean'] = balanced_data['text_clean'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
balanced_data['text_clean'] = balanced_data['text_clean'].str.lower().str.strip()

# Split the balanced data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    balanced_data['text_clean'], balanced_data['polarity'], test_size=0.1, random_state=42
)

# Create a pipeline with TfidfVectorizer and LogisticRegression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=10000)),
    ('classifier', LogisticRegression(max_iter=1000))
])

# Train the model
pipeline.fit(X_train, y_train)

# Validate the model
val_predictions = pipeline.predict(X_val)
val_accuracy = accuracy_score(y_val, val_predictions)
print(f'Validation accuracy: {val_accuracy}')

# Save the model and vectorizer to disk for later use
import joblib
joblib.dump(pipeline, 'sentiment_model.joblib')
