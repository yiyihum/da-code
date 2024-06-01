import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

# Load the training data
train = pd.read_csv('train.csv')

# Drop the extra 'id' column
train = train.drop(['id.1'], axis=1)

# Split the data into features and target variable
X = train.drop(['id', 'smoking'], axis=1)
y = train['smoking']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict the validation set results
y_pred = clf.predict_proba(X_val)[:, 1]

# Calculate the roc_auc_score
roc_auc = roc_auc_score(y_val, y_pred)
print(f'ROC AUC Score: {roc_auc}')

# Load the test data
test = pd.read_csv('test.csv')

# Predict the test set results
test['smoking'] = clf.predict_proba(test.drop('id', axis=1))[:, 1]

# Write the results into submission.csv
test[['id', 'smoking']].to_csv('submission.csv', index=False)
