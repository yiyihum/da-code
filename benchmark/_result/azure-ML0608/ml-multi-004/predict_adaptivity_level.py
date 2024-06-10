import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('students_adaptability_level_online_education.csv')

# Preprocess the data: Encode categorical features
label_encoders = {}
for column in train_data.columns[:-1]:  # Exclude the target column
    le = LabelEncoder()
    train_data[column] = le.fit_transform(train_data[column])
    label_encoders[column] = le

# Separate features and target
X = train_data.drop('Adaptivity Level', axis=1)
y = train_data['Adaptivity Level']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f'Validation Accuracy: {accuracy}')

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess the test data using the same label encoders
for column in test_data.columns:
    le = label_encoders[column]
    test_data[column] = le.transform(test_data[column])

# Predict the adaptivity level for the test data
predictions = model.predict(test_data)

# Save the predictions to a CSV file
output = pd.DataFrame(predictions, columns=['Adaptivity Level'])
output.to_csv('/workspace/level.csv', index=False)
