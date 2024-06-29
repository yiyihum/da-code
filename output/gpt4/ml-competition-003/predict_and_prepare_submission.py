import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')
train_data = train_data.loc[:, ~train_data.columns.duplicated()]
X_train = train_data.drop(columns=['id', 'Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults'])
y_train = train_data[['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']]

# Initialize and train the Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data in the same way as the training data
X_test = test_data.drop(columns=['Id'])
X_test = pd.get_dummies(X_test)

# Ensure that all columns in the training data are present in the test data
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

# Predict the probabilities for each class
test_probabilities = rf_classifier.predict_proba(X_test)

# Extract the probabilities for the positive class for each fault type
class_probabilities = {class_name: probs[:, 1] for class_name, probs in zip(y_train.columns, test_probabilities)}

# Create the submission dataframe
submission_df = pd.DataFrame(class_probabilities)
submission_df.insert(0, 'Id', test_data['Id'])

# Save the submission file
submission_df.to_csv('/workspace/submission.csv', index=False)
