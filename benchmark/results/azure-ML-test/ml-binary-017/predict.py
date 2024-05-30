import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import log_loss
from sklearn.preprocessing import StandardScaler

# Load the datasets
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

# Convert Class column to numeric
class_mapping = {'A': 0, 'B': 1}
train_df['Class'] = train_df['Class'].map(class_mapping)

# Store Ids for test data
test_ids = test_df['Id']

# Check for any non-numeric data and convert it to numeric if possible
non_numeric_columns = train_df.select_dtypes(include=['object']).columns
train_df = pd.get_dummies(train_df, columns=non_numeric_columns)
test_df = pd.get_dummies(test_df, columns=non_numeric_columns)

# Separate features and target from training data
X = train_df.drop(['Id', 'Class'], axis=1)
y = train_df['Class']

# Ensure the test dataframe has the same feature columns as the training dataframe
test_df = test_df.reindex(columns=X.columns, fill_value=0)

# Add 'Id' back to test dataframe
test_df['Id'] = test_ids

# Preprocess the data: scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data for training and validation
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Validate the model
y_val_pred_proba = clf.predict_proba(X_val)
val_log_loss = log_loss(y_val, y_val_pred_proba)
print(f"Validation Log Loss: {val_log_loss}")

# Prepare test data
X_test = test_df.drop(['Id'], axis=1)
X_test_scaled = scaler.transform(X_test)

# Predict on test data
y_test_pred_proba = clf.predict_proba(X_test)

# Generate submission file
submission = pd.DataFrame(y_test_pred_proba, columns=['class_0', 'class_1'])
submission['Id'] = test_ids
submission = submission[['Id', 'class_0', 'class_1']]
submission.to_csv('submission.csv', index=False)