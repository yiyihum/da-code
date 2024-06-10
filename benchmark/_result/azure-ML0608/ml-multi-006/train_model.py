import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import cross_val_score

# Load the preprocessed training and validation data
X_train = pd.read_csv('/workspace/X_train.csv')
y_train = pd.read_csv('/workspace/y_train.csv')
X_val = pd.read_csv('/workspace/X_val.csv')
y_val = pd.read_csv('/workspace/y_val.csv')

# Initialize the Random Forest classifier with fewer estimators to reduce training time
rf_classifier = RandomForestClassifier(n_estimators=50, random_state=42)

# Train the classifier
rf_classifier.fit(X_train, y_train.values.ravel())

# Predict on the validation set
y_pred = rf_classifier.predict(X_val)

# Evaluate the classifier
print("Validation Set Accuracy: ", accuracy_score(y_val, y_pred))
print("Classification Report:\n", classification_report(y_val, y_pred))

# Perform cross-validation to check for overfitting
cv_scores = cross_val_score(rf_classifier, X_train, y_train.values.ravel(), cv=5)
print("Cross-validation scores: ", cv_scores)
print("Mean cross-validation score: ", cv_scores.mean())

# Save the trained model for later use
import joblib
joblib.dump(rf_classifier, '/workspace/rf_classifier.joblib')

print("Model training and evaluation complete. Model saved.")
