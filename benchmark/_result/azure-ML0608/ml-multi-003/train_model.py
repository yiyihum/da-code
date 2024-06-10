import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Load the preprocessed data
X_train_vec = joblib.load('/workspace/X_train_vec.joblib')
y_train = joblib.load('/workspace/y_train.joblib')
X_test_vec = joblib.load('/workspace/X_test_vec.joblib')

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train_vec, y_train, test_size=0.2, random_state=42)

# Train a Random Forest Classifier with a very small number of estimators to save time
rf_clf = RandomForestClassifier(n_estimators=10, random_state=42)  # Reduced number of estimators to 10
rf_clf.fit(X_train, y_train)

# Validate the model
y_val_pred = rf_clf.predict(X_val)
val_accuracy = accuracy_score(y_val, y_val_pred)
print(f'Validation Accuracy: {val_accuracy}')

# Save the trained model
joblib.dump(rf_clf, '/workspace/rf_clf.joblib')
print('Model training complete and model saved.')
