import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv('students_adaptability_level_online_education.csv')

# Preprocess the dataset: Encode categorical features
label_encoders = {}
for column in data.columns[:-1]:  # Exclude the target column
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

# Separate features and target
X = data.drop('Adaptivity Level', axis=1)
y = data['Adaptivity Level']

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier(random_state=42)

# Train the model
rf_classifier.fit(X_train, y_train)

# Validate the model
y_pred = rf_classifier.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f"Validation Accuracy: {accuracy}")

# Load the test dataset
test_data = pd.read_csv('test.csv')

# Preprocess the test dataset: Encode categorical features using the same encoders
for column in test_data.columns:
    test_data[column] = label_encoders[column].transform(test_data[column])

# Make predictions on the test dataset
test_predictions = rf_classifier.predict(test_data)

# Save the predictions to a CSV file
test_data['Adaptivity Level'] = test_predictions
test_data[['Adaptivity Level']].to_csv('level.csv', index=False)
