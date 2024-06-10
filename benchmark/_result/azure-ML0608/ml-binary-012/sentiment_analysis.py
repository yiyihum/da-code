import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

# Load the training data
train_df = pd.read_csv('training.1600000.processed.noemoticon.csv', encoding='latin1', header=None, usecols=[0, 5], names=['polarity', 'text'])

# Preprocessing the text data
train_df['text'] = train_df['text'].str.replace(r'http\S+', '', regex=True).str.replace(r'@\w+', '', regex=True).str.replace(r'[^A-Za-z\s]', '', regex=True).str.lower()

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(train_df['text'], train_df['polarity'], test_size=0.1, random_state=42)

# Create a text processing and classification pipeline
pipeline = make_pipeline(
    CountVectorizer(),
    MultinomialNB()
)

# Train the model
pipeline.fit(X_train, y_train)

# Validate the model
y_pred = pipeline.predict(X_val)
print(f'Validation accuracy: {accuracy_score(y_val, y_pred)}')

# Load the test data
test_df = pd.read_csv('testdata.manual.2009.06.14.csv', encoding='latin1', header=None, usecols=[2, 4], names=['query', 'text'])

# Preprocessing the text data
test_df['text'] = test_df['text'].str.replace(r'http\S+', '', regex=True).str.replace(r'@\w+', '', regex=True).str.replace(r'[^A-Za-z\s]', '', regex=True).str.lower()

# Predict the sentiment
test_df['emotion'] = pipeline.predict(test_df['text'])

# Save the predictions to a CSV file
test_df[['emotion']].to_csv('sentiment.csv', index=False)
