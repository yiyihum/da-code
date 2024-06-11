from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=0)

# Fit the model to the training data
model.fit(X_train, y_train)

# Predict on the validation set
y_pred = model.predict(X_valid)

# Calculate the accuracy
accuracy = accuracy_score(y_valid, y_pred)
print(f"Validation accuracy: {accuracy:.4f}")
