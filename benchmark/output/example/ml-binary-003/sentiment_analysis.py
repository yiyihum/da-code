import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the training data
train_data = pd.read_csv('twitter_training.csv')

# Preprocessing function
def preprocess_text(text):
    if not isinstance(text, str):
        return ''
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if not word in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

# Preprocess the text data
train_data['text'] = train_data['text'].apply(preprocess_text)

# Remove rows with empty 'text' after preprocessing
train_data = train_data[train_data['text'].str.strip().astype(bool)]

# Encode the labels
label_encoder = LabelEncoder()
train_data['label'] = label_encoder.fit_transform(train_data['label'])

# Create a pipeline with a TF-IDF vectorizer and a logistic regression classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression(solver='liblinear'))
])

# Train the model
pipeline.fit(train_data['text'], train_data['label'])

# Load the validation data
validation_data = pd.read_csv('twitter_validation.csv')

# Preprocess the validation text data
validation_data['text'] = validation_data['text'].apply(preprocess_text)

# Predict the sentiment for each text in the validation set
predictions = pipeline.predict(validation_data['text'])

# Map the encoded labels back to the original labels
predictions = label_encoder.inverse_transform(predictions)

# Save the predictions to prediction.csv
result_df = pd.DataFrame(predictions, columns=['result'])
result_df.to_csv('prediction.csv', index=False)
