import pandas as pd
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import nltk

# Function to clean the tweet text
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove special characters and numbers
    text = re.sub('[^A-Za-z]+', ' ', text)
    # Remove single characters
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to preprocess the text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Clean the text
    text = clean_text(text)
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Stemming
    stemmer = SnowballStemmer('english')
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

# Load the test data
df_test = pd.read_csv('/workspace/Corona_NLP_test.csv', usecols=['OriginalTweet'])

# Preprocess the tweets
df_test['ProcessedTweet'] = df_test['OriginalTweet'].apply(preprocess_text)

# Initialize the Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

# Function to assign sentiment category
def assign_sentiment_category(score):
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Predict sentiment
df_test['Sentiment'] = df_test['ProcessedTweet'].apply(lambda x: assign_sentiment_category(sia.polarity_scores(x)['compound']))

# Save the predicted sentiments to a CSV file
df_test[['Sentiment']].to_csv('/workspace/sentiment.csv', index=False)
