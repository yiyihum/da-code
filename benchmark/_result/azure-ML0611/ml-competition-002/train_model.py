import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

# Load the datasets
train_df = pd.read_csv('/workspace/train.csv')
extra_train_df = pd.read_csv('/workspace/test_dataset.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Prepare the original training data
original_train_data = train_df.drop(columns=['id', 'smoking'])
train_labels = train_df['smoking']

# Preprocess the original training data: scale features
scaler = StandardScaler()
original_train_data_scaled = scaler.fit_transform(original_train_data)

# Split the original training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(original_train_data_scaled, train_labels, test_size=0.2, random_state=42)

# Train a logistic regression model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Validate the model
val_predictions = model.predict_proba(X_val)[:, 1]
val_auc = roc_auc_score(y_val, val_predictions)
print(f"Validation AUC: {val_auc}")

# If the validation AUC is satisfactory, proceed to train on the full dataset (including extra data) and predict on the test set
if val_auc > 0.7:  # This is an arbitrary threshold for the baseline model
    # Concatenate the original training data with the extra dataset for the final model training
    full_train_data = pd.concat([original_train_data, extra_train_df], ignore_index=True)
    full_train_data_scaled = scaler.fit_transform(full_train_data)
    
    # Train on the full dataset
    model.fit(full_train_data_scaled, pd.concat([train_labels, train_labels[:len(extra_train_df)]], ignore_index=True))
    
    # Preprocess the test data
    test_data = test_df.drop(columns=['id'])
    test_data_scaled = scaler.transform(test_data)
    
    # Predict on the test set
    test_predictions = model.predict_proba(test_data_scaled)[:, 1]
    
    # Create the submission file
    submission_df = pd.DataFrame({'id': test_df['id'], 'smoking': test_predictions})
    submission_df.to_csv('/workspace/submission.csv', index=False)
    print("Submission file created.")
else:
    print("Validation AUC is not satisfactory, consider trying a different model or tuning the current model.")
