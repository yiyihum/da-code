import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Load the datasets
true_news = pd.read_csv('True.csv')
fake_news = pd.read_csv('Fake.csv')

# Combine the datasets
news = pd.concat([true_news, fake_news], ignore_index=True)

# Preprocess the data
# Using 'text' column for prediction, you can also consider using 'title' or both
X = news['text']
y = news['label']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a TF-IDF Vectorizer and Logistic Regression pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LogisticRegression(solver='liblinear'))
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")

# Load the validation dataset
validation_data = pd.read_csv('validation.csv')

# Predict the authenticity of the news in validation.csv
validation_data['result'] = pipeline.predict(validation_data['text'])

# Write the prediction results into result.csv
validation_data[['result']].to_csv('result.csv', index=False)
