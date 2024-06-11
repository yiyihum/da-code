import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

# Load the training data
def load_data(filename):
    data = []
    labels = []
    with open(filename, 'r') as file:
        for line in file:
            text, label = line.strip().split(';')
            data.append(text)
            labels.append(label)
    return data, labels

# Preprocess and split the data
data, labels = load_data('train.txt')
train_data, val_data, train_labels, val_labels = train_test_split(data, labels, test_size=0.2, random_state=42)

# Create a model pipeline
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(train_data, train_labels)

# Validate the model
val_predictions = model.predict(val_data)
val_accuracy = accuracy_score(val_labels, val_predictions)
print(f"Validation Accuracy: {val_accuracy}")

# Save the model to a file
import joblib
joblib.dump(model, 'emotion_classifier.joblib')
