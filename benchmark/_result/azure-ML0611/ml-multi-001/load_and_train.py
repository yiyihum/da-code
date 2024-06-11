import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv('/workspace/activities.csv')

# Check for any missing values
print(data.isnull().sum().sum(), "missing values in the dataset.")

# Split the dataset into features and labels
X = data.drop(columns=['Activity'])
y = data['Activity']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
rf_classifier.fit(X_train, y_train)

# Validate the classifier
y_pred = rf_classifier.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f"Validation accuracy: {accuracy}")

# Save the trained model to a file
import joblib
joblib.dump(rf_classifier, '/workspace/rf_classifier.joblib')
