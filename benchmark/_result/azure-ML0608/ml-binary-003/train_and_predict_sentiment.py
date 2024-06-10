import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Load the datasets
training_data = pd.read_csv('twitter_training.csv')
validation_data = pd.read_csv('twitter_validation.csv')

# Preprocess the training data: Convert 'Irrelevant' labels to 'Neutral'
training_data['label'] = training_data['label'].replace('Irrelevant', 'Neutral')

# Handle NaN values in the text column by replacing them with an empty string
training_data = training_data.fillna({'text': ''})
validation_data = validation_data.fillna({'text': ''})

# Split the training data into features and target labels
X_train = training_data['text']
y_train = training_data['label']

# Create a text classification pipeline with CountVectorizer and MultinomialNB
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Predict the sentiment for the validation dataset
validation_predictions = model.predict(validation_data['text'])

# Save the predictions to prediction.csv with the column name 'result'
prediction_df = pd.DataFrame(validation_predictions, columns=['result'])
prediction_df.to_csv('prediction.csv', index=False)
