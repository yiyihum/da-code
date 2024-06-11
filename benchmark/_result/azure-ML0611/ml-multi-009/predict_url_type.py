import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Load the dataset
data = pd.read_csv('malicious_phish.csv')

# Sample a smaller subset of the data for quicker training
data_sample = data.sample(frac=0.1, random_state=42)

# Preprocessing
# Extract the input features and the target variable
X = data_sample['url']
y = data_sample['type']

# Create a machine learning pipeline
pipeline = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB()
)

# Train the model
pipeline.fit(X, y)

# Load the test data
test_data = pd.read_csv('test.csv', header=None, names=['url'])

# Predict the type of the URLs in the test data
test_data['type'] = pipeline.predict(test_data['url'])

# Save the predictions to a CSV file
test_data[['type']].to_csv('type.csv', index=False)
