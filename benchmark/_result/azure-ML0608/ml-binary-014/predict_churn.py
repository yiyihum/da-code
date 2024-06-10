import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocess the data: Encode categorical variables
label_encoders = {}
for column in train_data.columns:
    if train_data[column].dtype == object and column != 'CustomerID':
        le = LabelEncoder()
        train_data[column] = le.fit_transform(train_data[column])
        label_encoders[column] = le

# Separate features and target variable
X = train_data.drop(['CustomerID', 'Churn'], axis=1)
y = train_data['Churn']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f'Validation Accuracy: {accuracy}')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data using the same label encoders
for column in label_encoders:
    test_data[column] = label_encoders[column].transform(test_data[column])

# Predict churn for the test data
X_test = test_data.drop(['CustomerID'], axis=1)
test_data['Churn'] = model.predict(X_test)

# Save the predictions to churn.csv
test_data[['CustomerID', 'Churn']].to_csv('/workspace/churn.csv', index=False)
