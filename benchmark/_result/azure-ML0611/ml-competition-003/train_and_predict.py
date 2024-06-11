import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Remove the duplicate 'id.1' column
train_data.drop(columns=['id.1'], inplace=True)

# Combine the target variables into a single binary class
condition_columns = ['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']
train_data['Class'] = train_data[condition_columns].max(axis=1)
train_data.drop(columns=condition_columns, inplace=True)

# Split the data into features and labels
X_train = train_data.drop(columns=['Class', 'id'])
y_train = train_data['Class']

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_classifier.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data to have the same features as the training data
# Assuming that the test data should have the same features as the training data, except for the target and 'id' columns
X_test = test_data[X_train.columns]

# Predict using the trained Random Forest model
test_predictions = rf_classifier.predict_proba(X_test)

# Create a submission dataframe
submission = pd.DataFrame({
    'Id': test_data['Id'],
    'class_0': test_predictions[:, 0],
    'class_1': test_predictions[:, 1]
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)

# Output the path to the submission file
print("/workspace/submission.csv")
