import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Explicitly drop the 'id.1' column if it exists
if 'id.1' in train_data.columns:
    train_data = train_data.drop(columns=['id.1'])

# Separate features and targets
X = train_data.drop(columns=['id', 'Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults'])
y = train_data[['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']]

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)

# Train a model for each defect category
models = {}
for defect in y.columns:
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train[defect])
    models[defect] = model

# Validate the models
auc_scores = {}
for defect, model in models.items():
    y_pred_prob = model.predict_proba(X_val)[:, 1]
    auc_score = roc_auc_score(y_val[defect], y_pred_prob)
    auc_scores[defect] = auc_score

# Average AUC score
average_auc = sum(auc_scores.values()) / len(auc_scores)
print(f'Average AUC score on the validation set: {average_auc}')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')
X_test = test_data.drop(columns=['id'])
X_test = scaler.transform(X_test)

# Make predictions on the test data
predictions = pd.DataFrame(test_data['id'], columns=['id'])
for defect, model in models.items():
    predictions[defect] = model.predict_proba(X_test)[:, 1]

# Save the predictions to a CSV file
predictions.to_csv('/workspace/submission.csv', index=False)
