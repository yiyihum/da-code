import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load the training and test data
train_data = pd.read_csv('Date_Fruit_Datasets.csv')
test_data = pd.read_csv('test.csv')

# Separate features and target variable from the training data
X_train = train_data.drop('Class', axis=1)
y_train = train_data['Class']
X_test = test_data

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the Random Forest Classifier
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train_scaled, y_train)

# Predict on the test data
y_test_pred = rf_clf.predict(X_test_scaled)

# Save the predictions to a CSV file
predictions = pd.DataFrame(y_test_pred, columns=['Class'])
predictions.to_csv('class.csv', index=False)
print("Predictions saved to class.csv")
