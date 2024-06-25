import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

# Load the training data
train_df = pd.read_csv('uci-news-aggregator.csv')

# Preprocess the data: Use only 'TITLE' and 'CATEGORY'
train_df = train_df[['TITLE', 'CATEGORY']]

# Split the training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    train_df['TITLE'], train_df['CATEGORY'], test_size=0.1, random_state=42
)

# Create a text processing and machine learning pipeline
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
val_accuracy = accuracy_score(y_val, y_pred)
print(f"Validation accuracy: {val_accuracy}")

# Load the test data
test_df = pd.read_csv('test.csv')

# Predict the categories for the test data
test_df['CATEGORY'] = model.predict(test_df['TITLE'])

# Save the predicted results into category.csv
test_df[['ID', 'CATEGORY']].to_csv('category.csv', index=False)
