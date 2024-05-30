import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the training data
training_data = pd.read_csv('customer_churn_dataset-training-master.csv')

# Drop rows with NaN values in the 'Churn' column
training_data = training_data.dropna(subset=['Churn'])

# Preprocessing the training data
# Convert categorical variables using label encoding
label_encoder = LabelEncoder()
for column in training_data.columns:
    if training_data[column].dtype == 'object':
        training_data[column] = label_encoder.fit_transform(training_data[column])

# Separate features and labels
X_train = training_data.drop(['CustomerID', 'Churn'], axis=1)
y_train = training_data['Churn']

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Load the testing data
test_data = pd.read_csv('customer_churn_dataset-testing-master.csv')

# Apply the same preprocessing to the test data
for column in test_data.columns:
    if test_data[column].dtype == 'object':
        # Transform using label encoding
        test_data[column] = label_encoder.fit_transform(test_data[column])

# Remove the 'CustomerID' column as it's not a feature
X_test = test_data.drop('CustomerID', axis=1)

# Predict churn
predictions = model.predict(X_test)

# Save the results
result = pd.DataFrame({'CustomerID': test_data['CustomerID'], 'result': predictions})
result.to_csv('result.csv', index=False)