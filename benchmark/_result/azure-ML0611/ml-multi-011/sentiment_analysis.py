import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Load the test dataset with ISO-8859-1 encoding
test_data = pd.read_csv('/workspace/Corona_NLP_test.csv', encoding='ISO-8859-1')

# Map the sentiment labels to the required format
sentiment_mapping = {
    'Extremely Negative': 'Negative',
    'Negative': 'Negative',
    'Neutral': 'Neutral',
    'Positive': 'Positive',
    'Extremely Positive': 'Positive'
}
test_data['Sentiment'] = test_data['Sentiment'].map(sentiment_mapping)

# Load the training dataset with ISO-8859-1 encoding
train_data = pd.read_csv('/workspace/Corona_NLP_train.csv', encoding='ISO-8859-1')
train_data['Sentiment'] = train_data['Sentiment'].map(sentiment_mapping)

# Extract features and labels
X_train = train_data['OriginalTweet']
y_train = train_data['Sentiment']
X_test = test_data['OriginalTweet']

# Text vectorization
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train a Naive Bayes classifier
nb_classifier = MultinomialNB()
nb_classifier.fit(X_train_vectorized, y_train)

# Predict the sentiment of the test data
y_pred = nb_classifier.predict(X_test_vectorized)

# Save the predictions to a CSV file
predictions = pd.DataFrame(y_pred, columns=['Sentiment'])
predictions.to_csv('/workspace/sentiment.csv', index=False)

# Print the first few predictions
print(predictions.head())
