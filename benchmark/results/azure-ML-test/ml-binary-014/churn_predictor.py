import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load and preprocess the training data
train_data = pd.read_csv('train.csv')
features = train_data.drop(columns=['CustomerID', 'Churn'])
target = train_data['Churn']
label_encoders = {}

# Encode categorical variables
for column in features.select_dtypes(include=['object']).columns:
    label_encoders[column] = LabelEncoder()
    features[column] = label_encoders[column].fit_transform(features[column])

# Train the model
model = RandomForestClassifier(random_state=0)
model.fit(features, target)

# Load and preprocess the test data
test_data = pd.read_csv('test.csv')
test_features = test_data.drop(columns=['CustomerID'])
test_ids = test_data['CustomerID']

# Apply the same encoding to the test data
for column in test_features.select_dtypes(include=['object']).columns:
    le = label_encoders.get(column)
    if le:
        test_features[column] = le.transform(test_features[column])
    else:
        # If the label encoder was not used before, fit it on the test data
        test_features[column] = LabelEncoder().fit_transform(test_features[column])

# Predict the churn values
test_predictions = model.predict(test_features)

# Save the predictions
prediction_output = pd.DataFrame({'CustomerID': test_ids, 'Churn': test_predictions})
prediction_output.to_csv('churn.csv', index=False)