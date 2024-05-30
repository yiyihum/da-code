import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('train_u6lujuX_CVtuZ9i.csv')

# Preprocess the data by encoding categorical variables
X = pd.get_dummies(train_data.drop(columns=['Loan_Status', 'Loan_ID']), drop_first=True)
y = train_data['Loan_Status'].apply(lambda x: 1 if x == 'Y' else 0)  # Encode target as 0 and 1

# Split the training data for model validation (train/validation sets)
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the classifier
classifier = RandomForestClassifier(random_state=42)
classifier.fit(X_train, y_train)

# Validate the model
predictions = classifier.predict(X_valid)
accuracy = accuracy_score(y_valid, predictions)
print(f'Validation accuracy: {accuracy}')

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess test data to match training data format
X_test = pd.get_dummies(test_data.drop(columns=['Loan_ID']), drop_first=True)

# Ensure all columns in the training data are in the test data
X_test = X_test.reindex(columns=X.columns, fill_value=0)

# Make predictions on the test data
test_predictions = classifier.predict(X_test)

# Convert predictions back to 'Y' and 'N'
test_predictions = ['Y' if pred == 1 else 'N' for pred in test_predictions]

# Create a DataFrame with the Loan_ID and the predictions
result = pd.DataFrame({'Loan_ID': test_data['Loan_ID'], 'Loan_Status': test_predictions})

# Write the result to a CSV file
result.to_csv('result.csv', index=False)