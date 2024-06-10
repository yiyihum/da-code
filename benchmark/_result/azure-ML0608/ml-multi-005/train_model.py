import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

# Load the dataset
data = pd.read_csv('/workspace/train.txt', sep=';', header=None, names=['text', 'emotion'])

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(data['text'], data['emotion'], test_size=0.2, random_state=42)

# Create a text processing and classification pipeline
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
print(classification_report(y_val, y_pred))

# Save the model to a file
import joblib
joblib.dump(model, '/workspace/emotion_classifier.joblib')
