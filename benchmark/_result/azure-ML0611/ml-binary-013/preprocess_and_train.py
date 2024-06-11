import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the training data
train_data = pd.read_csv('/workspace/Train.csv')

# Impute missing values with mean
train_data.fillna(train_data.mean(), inplace=True)

# Check if missing values are filled
print(train_data.isnull().sum())

# Split the data into features and target variable
X = train_data.drop('Target', axis=1)
y = train_data['Target']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the classifier
rf_classifier.fit(X_train, y_train)

# Validate the classifier
y_pred = rf_classifier.predict(X_val)
print(classification_report(y_val, y_pred))
print(f"Accuracy: {accuracy_score(y_val, y_pred)}")

# Save the trained model
joblib.dump(rf_classifier, '/workspace/rf_classifier.joblib')
