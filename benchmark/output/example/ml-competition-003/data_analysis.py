import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import log_loss
from sklearn.preprocessing import OneHotEncoder

# Load datasets
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# Save the 'Id' column of the test dataset for later use
test_id = test['Id']

# One-hot encode the 'EJ' column
encoder = OneHotEncoder()
train_EJ_encoded = pd.DataFrame(encoder.fit_transform(train[['EJ']]).toarray())
test_EJ_encoded = pd.DataFrame(encoder.transform(test[['EJ']]).toarray())

# Add the encoded 'EJ' column back to the datasets
train = pd.concat([train, train_EJ_encoded], axis=1)
test = pd.concat([test, test_EJ_encoded], axis=1)

# Drop the original 'EJ' column
train = train.drop('EJ', axis=1)
test = test.drop('EJ', axis=1)

# Convert all feature names to strings
train.columns = train.columns.astype(str)
test.columns = test.columns.astype(str)

# Drop the 'Id' and 'Id.1' columns
train = train.drop(['Id', 'Id.1'], axis=1)
test = test.drop('Id', axis=1)

# Split the training data into training and validation sets
X = train.drop('Class', axis=1)
y = train['Class']
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_val_pred = model.predict_proba(X_val)
print('Validation Log Loss:', log_loss(y_val, y_val_pred))

# Predict the test data
predictions = model.predict_proba(test)

# Write the results into submission.csv
submission = pd.DataFrame(predictions, columns=['class_0', 'class_1'])
submission.insert(0, 'Id', test_id)
submission.to_csv('submission.csv', index=False)
