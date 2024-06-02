import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import log_loss

# Load the training data
train_data = pd.read_csv('train.csv')

# Preprocess the training data
train_data['Drug'] = LabelEncoder().fit_transform(train_data['Drug'])
train_data['Sex'] = LabelEncoder().fit_transform(train_data['Sex'])
train_data['Ascites'] = LabelEncoder().fit_transform(train_data['Ascites'])
train_data['Hepatomegaly'] = LabelEncoder().fit_transform(train_data['Hepatomegaly'])
train_data['Spiders'] = LabelEncoder().fit_transform(train_data['Spiders'])
train_data['Edema'] = LabelEncoder().fit_transform(train_data['Edema'])
train_data['Status'] = LabelEncoder().fit_transform(train_data['Status'])

# Split the training data into training set and validation set
X_train, X_val, y_train, y_val = train_test_split(train_data.drop(['id', 'Status'], axis=1), train_data['Status'], test_size=0.2, random_state=42)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Validate the classifier
y_val_pred = clf.predict_proba(X_val)
print('Validation Log Loss:', log_loss(y_val, y_val_pred))

# Load the testing data
test_data = pd.read_csv('test.csv')

# Preprocess the testing data
test_data['Drug'] = LabelEncoder().fit_transform(test_data['Drug'])
test_data['Sex'] = LabelEncoder().fit_transform(test_data['Sex'])
test_data['Ascites'] = LabelEncoder().fit_transform(test_data['Ascites'])
test_data['Hepatomegaly'] = LabelEncoder().fit_transform(test_data['Hepatomegaly'])
test_data['Spiders'] = LabelEncoder().fit_transform(test_data['Spiders'])
test_data['Edema'] = LabelEncoder().fit_transform(test_data['Edema'])

# Predict the outcomes of the testing data
y_test_pred = clf.predict_proba(test_data.drop('id', axis=1))

# Create the submission file
submission = pd.DataFrame(y_test_pred, columns=['Status_C', 'Status_CL', 'Status_D'])
submission.insert(0, 'id', test_data['id'])
submission.to_csv('submission.csv', index=False)
