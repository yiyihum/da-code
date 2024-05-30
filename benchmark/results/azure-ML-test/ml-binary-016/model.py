import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

# Load the datasets
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Separate features and target from training data
X_train = train_data.drop(columns=['id', 'smoking'])
y_train = train_data['smoking']

# Preprocess the data: scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Split the training data for validation
X_train_part, X_val_part, y_train_part, y_val_part = train_test_split(
    X_train_scaled, y_train, test_size=0.2, random_state=42)

# Initialize and train the classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train_part, y_train_part)

# Predict on validation part
y_val_pred = classifier.predict_proba(X_val_part)[:, 1]

# Evaluate the model
auc_score = roc_auc_score(y_val_part, y_val_pred)
print(f'Validation AUC: {auc_score}')

# Prepare the test set for prediction
X_test = test_data.drop(columns=['id'])
X_test_scaled = scaler.transform(X_test)

# Predict on test data
test_pred = classifier.predict_proba(X_test_scaled)[:, 1]

# Create the submission file
submission = pd.DataFrame({
    'id': test_data['id'],
    'smoking': test_pred
})
submission.to_csv('submission.csv', index=False)