import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# Load the training data
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# Store test ids for the submission file
test_ids = test['id']

# Drop unnecessary columns
train.drop(['id', 'CustomerId', 'Surname', 'id.1'], axis=1, inplace=True)
test.drop(['id', 'CustomerId', 'Surname'], axis=1, inplace=True)

# One-hot encode categorical variables
train = pd.get_dummies(train)
test = pd.get_dummies(test)

# Split features and target
X = train.drop('Exited', axis=1)
y = train['Exited']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Validate the model
y_pred = clf.predict_proba(X_val)[:, 1]
print(f'Validation ROC-AUC score: {roc_auc_score(y_val, y_pred)}')

# Predict on the test set
test_predictions = clf.predict_proba(test)[:, 1]

# Prepare the submission file
submission = pd.DataFrame({'id': test_ids, 'Exited': test_predictions})
submission.to_csv('submission.csv', index=False)
