import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the dataset
data = pd.read_csv('diabetes_prediction_dataset.csv')

# Preprocess the data: Encode categorical variables
label_encoders = {}
for column in ['gender', 'smoking_history']:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

# Split the data into features and target
X = data.drop('diabetes', axis=1)
y = data['diabetes']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f"Validation Accuracy: {accuracy}")

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess the test data using the same label encoders
for column in ['gender', 'smoking_history']:
    test_data[column] = label_encoders[column].transform(test_data[column])

# Make predictions on the test data
test_predictions = model.predict(test_data)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(test_predictions, columns=['diabetes'])
predictions_df.to_csv('diabetes.csv', index=False)
