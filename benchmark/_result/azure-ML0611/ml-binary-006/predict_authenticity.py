import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Load the datasets
true_news = pd.read_csv('True.csv')
fake_news = pd.read_csv('Fake.csv')
validation_data = pd.read_csv('validation.csv')

# Combine the datasets
news_data = pd.concat([true_news, fake_news], ignore_index=True)

# Preprocess the data: Use 'text' column for prediction and 'label' as the target
X = news_data['text']
y = news_data['label']

# Split the data into training and test sets (although we won't use the test set here)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline with TfidfVectorizer and LogisticRegression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LogisticRegression(solver='liblinear'))
])

# Train the model
pipeline.fit(X_train, y_train)

# Predict on the validation set
validation_predictions = pipeline.predict(validation_data['text'])

# Save the predictions to a CSV file
result_df = pd.DataFrame(validation_predictions, columns=['result'])
result_df.to_csv('result.csv', index=False)
