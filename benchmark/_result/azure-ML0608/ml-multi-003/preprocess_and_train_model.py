import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(postings_df['text'], postings_df['encoded_experience_level'], test_size=0.2, random_state=42)

# Use a simple bag-of-words model for text features
vectorizer = CountVectorizer(stop_words='english', max_features=500)  # Reduced number of features
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)
X_test_vec = vectorizer.transform(test_df['text'])

# Train a Random Forest Classifier with fewer estimators
rf_clf = RandomForestClassifier(n_estimators=50, random_state=42)  # Reduced number of estimators
rf_clf.fit(X_train_vec, y_train)

# Validate the model
y_val_pred = rf_clf.predict(X_val_vec)
val_accuracy = accuracy_score(y_val, y_val_pred)
print(f'Validation Accuracy: {val_accuracy}')

# Predict on the test set
test_predictions = rf_clf.predict(X_test_vec)
test_df['formatted_experience_level'] = label_encoder.inverse_transform(test_predictions)

# Save the predictions to a CSV file
test_df[['job_id', 'formatted_experience_level']].to_csv('/workspace/result.csv', index=False)
print('Predictions saved to result.csv')
