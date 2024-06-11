import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# Load the training essays data
train_essays = pd.read_csv('/workspace/train_essays.csv')

# Drop the duplicate 'id' column
train_essays = train_essays.loc[:, ~train_essays.columns.duplicated()]

# Split the data into features and target
X = train_essays['text']
y = train_essays['generated']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)

# Train a logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Predict probabilities on the validation set
val_probabilities = model.predict_proba(X_val_tfidf)[:, 1]

# Calculate the ROC AUC score
roc_auc = roc_auc_score(y_val, val_probabilities)
print(f'Validation ROC AUC Score: {roc_auc}')

# Save the model and vectorizer for later use
import joblib
joblib.dump(model, '/workspace/llm_detection_model.pkl')
joblib.dump(vectorizer, '/workspace/llm_detection_vectorizer.pkl')

# Indicate success
print("Model and vectorizer saved successfully.")
