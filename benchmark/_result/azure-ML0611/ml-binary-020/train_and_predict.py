import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv('/workspace/CVD_cleaned.csv')

# Preprocessing
# Encode categorical variables
label_encoders = {}
for column in data.columns:
    if data[column].dtype == object:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le

# Separate features and target
X = data.drop('Heart_Disease', axis=1)
y = data['Heart_Disease']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Apply the same preprocessing to the test data
for column in test_data.columns:
    if column in label_encoders:
        le = label_encoders[column]
        test_data[column] = le.transform(test_data[column].astype(str))

# Make predictions on the test data
test_predictions = model.predict(test_data)

# Save the predictions to a CSV file
prediction_df = pd.DataFrame(test_predictions, columns=['Heart_Disease'])
prediction_df.to_csv('/workspace/disease.csv', index=False)
