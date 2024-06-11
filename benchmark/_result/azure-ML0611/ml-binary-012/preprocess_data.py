import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Load the training data
training_data_path = 'training.1600000.processed.noemoticon.csv'
training_columns = ['polarity', 'id', 'date', 'query', 'user', 'text']
training_data = pd.read_csv(training_data_path, encoding='latin1', names=training_columns)

# Preprocess the text data: remove URLs, mentions, and non-alphabetic characters
training_data['text_clean'] = training_data['text'].str.replace(r'http\S+', '', regex=True)
training_data['text_clean'] = training_data['text_clean'].str.replace(r'@\w+', '', regex=True)
training_data['text_clean'] = training_data['text_clean'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
training_data['text_clean'] = training_data['text_clean'].str.lower().str.strip()

# Split the training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    training_data['text_clean'], training_data['polarity'], test_size=0.1, random_state=42
)

# Vectorize the text using CountVectorizer
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_val_vectorized = vectorizer.transform(X_val)

# Train a logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vectorized, y_train)

# Validate the model
val_predictions = model.predict(X_val_vectorized)
val_accuracy = (val_predictions == y_val).mean()
print(f'Validation accuracy: {val_accuracy}')
