import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# Load the training data
train = pd.read_csv('train.csv')

# Separate features and target variables
X = train.drop(['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults', 'id', 'id.1'], axis=1)
y = train[['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']]

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model
model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_val_pred = model.predict_proba(X_val)
y_val_pred = np.concatenate([proba[:, 1].reshape(-1, 1) for proba in y_val_pred], axis=1)  # get the probability of the positive class
roc_auc = roc_auc_score(y_val, y_val_pred, average='macro')
print(f'Validation ROC-AUC: {roc_auc}')

# Load the test data
test = pd.read_csv('test.csv')

# Make predictions on the test set
X_test = test.drop(['id'], axis=1)
y_test_pred = model.predict_proba(X_test)
y_test_pred = np.concatenate([proba[:, 1].reshape(-1, 1) for proba in y_test_pred], axis=1)  # get the probability of the positive class

# Prepare the submission
submission = pd.DataFrame(y_test_pred)
submission.columns = ['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']
submission.insert(0, 'id', test['id'])
submission.to_csv('submission.csv', index=False)
