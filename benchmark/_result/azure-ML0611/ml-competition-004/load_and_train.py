import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and targets
features = train_data.drop(columns=['id', 'Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults'])
targets = train_data[['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']]

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(features, targets, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Train a Random Forest Classifier for each defect category and calculate AUC
auc_scores = []
for defect in targets.columns:
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_scaled, y_train[defect])
    y_pred_proba = clf.predict_proba(X_val_scaled)[:, 1]
    auc = roc_auc_score(y_val[defect], y_pred_proba)
    auc_scores.append(auc)
    print(f"AUC for {defect}: {auc}")

# Calculate the average AUC across all defect categories
average_auc = sum(auc_scores) / len(auc_scores)
print(f"Average AUC: {average_auc}")
