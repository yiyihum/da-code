import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

# Load the training data
train_data = pd.read_csv('train.csv')

# Split the data into features and target
X_train = train_data['full_text']
y_train = train_data['score']

# Create a simple text processing and Linear Regression pipeline
model = make_pipeline(CountVectorizer(), LinearRegression())

# Train the model
model.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('test.csv')

# Predict scores for the test data
predictions = model.predict(test_data['full_text'])

# Create a DataFrame for the submission
submission = pd.DataFrame({
    'essay_id': test_data['essay_id'],
    'score': predictions
})

# Round the predictions to the nearest integer as scores are integers
submission['score'] = submission['score'].round().astype(int)

# Save the submission file
submission.to_csv('submission.csv', index=False)

print("Submission file generated successfully.")
