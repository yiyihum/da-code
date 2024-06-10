import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline

# Load the training data
train_df = pd.read_csv('/workspace/train_essays.csv')

# Split the data into features and target
X = train_df['text']
y = train_df['generated']

# Split the data into training and validation sets with stratification
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Create a text processing and machine learning pipeline
pipeline = make_pipeline(
    TfidfVectorizer(stop_words='english', max_features=5000),
    RandomForestClassifier(n_estimators=100, random_state=42)
)

# Train the model
pipeline.fit(X_train, y_train)

# Validate the model
y_val_pred = pipeline.predict_proba(X_val)[:, 1]
val_auc = roc_auc_score(y_val, y_val_pred)
print(f'Validation AUC: {val_auc}')

# Load the test data
test_df = pd.read_csv('/workspace/test_essays.csv')

# Make predictions on the test data
test_predictions = pipeline.predict_proba(test_df['text'])[:, 1]

# Create the submission dataframe
submission_df = pd.DataFrame({
    'id': test_df['id'],
    'generated': test_predictions
})

# Save the submission file
submission_df.to_csv('/workspace/submission.csv', index=False)
