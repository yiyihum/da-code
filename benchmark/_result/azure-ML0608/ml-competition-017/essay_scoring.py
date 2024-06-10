import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Preprocess the data: Extract features and labels
X_train = train_df['full_text']
y_train = train_df['score']

# Convert the text data into numerical vectors using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_vect = vectorizer.fit_transform(X_train)

# Train a simple Linear Regression model
model = LinearRegression()
model.fit(X_train_vect, y_train)

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Preprocess the test data and make predictions
X_test = test_df['full_text']
X_test_vect = vectorizer.transform(X_test)
test_df['score'] = model.predict(X_test_vect)

# Ensure the predicted score is within the expected range (e.g., 0 to 6)
test_df['score'] = test_df['score'].clip(lower=0, upper=6)

# Write the predictions to a submission file
submission_df = test_df[['essay_id', 'score']]
submission_df.to_csv('/workspace/submission.csv', index=False)
