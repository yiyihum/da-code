import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Load the training and test data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Remove the 'id.1' column from the training data
train_data = train_data.drop(columns=['id.1'])

# Separate features and targets in training data
train_features = train_data.drop(columns=['id', 'Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults'])
train_targets = train_data[['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']]

# Features in test data
test_features = test_data.drop(columns=['id'])

# Standardize the features
scaler = StandardScaler()
train_features_scaled = scaler.fit_transform(train_features)
test_features_scaled = scaler.transform(test_features)

# Train a Random Forest Classifier for each defect category and make predictions on test data
submission = pd.DataFrame()
submission['id'] = test_data['id']
for defect in train_targets.columns:
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(train_features_scaled, train_targets[defect])
    submission[defect] = clf.predict_proba(test_features_scaled)[:, 1]

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
print("Submission file saved.")
