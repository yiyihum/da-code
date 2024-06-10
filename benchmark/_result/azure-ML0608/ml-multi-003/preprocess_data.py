import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer

# Load the datasets
postings_df = pd.read_csv('/workspace/postings.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Preprocessing the data
# Fill missing values in 'title' and 'description' with empty strings
postings_df['title'].fillna('', inplace=True)
postings_df['description'].fillna('', inplace=True)
test_df['title'].fillna('', inplace=True)
test_df['description'].fillna('', inplace=True)

# Combine 'title' and 'description' into a single feature for simplicity
postings_df['text'] = postings_df['title'] + ' ' + postings_df['description']
test_df['text'] = test_df['title'] + ' ' + test_df['description']

# Encode the target variable
label_encoder = LabelEncoder()
postings_df['encoded_experience_level'] = label_encoder.fit_transform(postings_df['formatted_experience_level'])

# Save the label encoder for later use
import joblib
joblib.dump(label_encoder, '/workspace/label_encoder.joblib')

# Use a simple bag-of-words model for text features
vectorizer = CountVectorizer(stop_words='english', max_features=500)  # Reduced number of features
X_train_vec = vectorizer.fit_transform(postings_df['text'])
X_test_vec = vectorizer.transform(test_df['text'])

# Save the vectorized text features and labels
joblib.dump(X_train_vec, '/workspace/X_train_vec.joblib')
joblib.dump(postings_df['encoded_experience_level'], '/workspace/y_train.joblib')
joblib.dump(X_test_vec, '/workspace/X_test_vec.joblib')

print('Preprocessing complete and data saved.')
