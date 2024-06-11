import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

# Load the training and validation datasets
train_df = pd.read_csv('twitter_training.csv')
validation_df = pd.read_csv('twitter_validation.csv')

# Preprocess the training data
# Map 'Irrelevant' sentiment to 'Neutral' as per README instructions
train_df['label'] = train_df['label'].replace('Irrelevant', 'Neutral')

# Handle NaN values in the text column
train_df['text'] = train_df['text'].fillna('')

# Encode the labels
label_encoder = LabelEncoder()
train_df['encoded_label'] = label_encoder.fit_transform(train_df['label'])

# Split the training data into features and target
X_train = train_df['text']
y_train = train_df['encoded_label']

# Create a text processing and machine learning pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('classifier', LogisticRegression(max_iter=1000))
])

# Train the model
pipeline.fit(X_train, y_train)

# Predict the sentiment labels for the validation data
validation_df['result'] = label_encoder.inverse_transform(pipeline.predict(validation_df['text']))

# Save the predictions to a CSV file
validation_df[['result']].to_csv('prediction.csv', index=False)
