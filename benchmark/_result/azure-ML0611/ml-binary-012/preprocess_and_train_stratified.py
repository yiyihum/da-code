import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Load a subset of the training data to avoid timeout
training_data_path = 'training.1600000.processed.noemoticon.csv'
training_columns = ['polarity', 'id', 'date', 'query', 'user', 'text']
nrows = 50000  # Load a subset of 50,000 rows
training_data = pd.read_csv(training_data_path, encoding='latin1', names=training_columns, nrows=nrows)

# Preprocess the text data: remove URLs, mentions, and non-alphabetic characters
training_data['text_clean'] = training_data['text'].str.replace(r'http\S+', '', regex=True)
training_data['text_clean'] = training_data['text_clean'].str.replace(r'@\w+', '', regex=True)
training_data['text_clean'] = training_data['text_clean'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
training_data['text_clean'] = training_data['text_clean'].str.lower().str.strip()

# Split the training data into training and validation sets with stratification
X_train, X_val, y_train, y_val = train_test_split(
    training_data['text_clean'], training_data['polarity'], test_size=0.1, random_state=42, stratify=training_data['polarity']
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
