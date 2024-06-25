import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss
import numpy as np

# Load the datasets again
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Encode categorical variables using one-hot encoding
train_data = pd.get_dummies(train_data, columns=['Drug', 'Sex', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema'])
test_data = pd.get_dummies(test_data, columns=['Drug', 'Sex', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema'])

# Ensure the order of column in the test set is in the same order than in train set
test_data = test_data[train_data.drop(columns=['Status']).columns]

# Split the data into features and target label
X = train_data.drop(columns=['id', 'Status'])
y = train_data['Status'].map({'C': 0, 'CL': 1, 'D': 2})  # Encode target labels

# Normalize the feature data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
test_data_scaled = scaler.transform(test_data.drop(columns=['id']))

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_scaled, y)

# Predict probabilities for the test set
test_probabilities = clf.predict_proba(test_data_scaled)

# Create a submission dataframe
submission = pd.DataFrame(test_probabilities, columns=['Status_C', 'Status_CL', 'Status_D'])
submission['id'] = test_data['id']
submission = submission[['id', 'Status_C', 'Status_CL', 'Status_D']]

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
