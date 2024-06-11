import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load the datasets
data = pd.read_csv('/workspace/data.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Split the training data into features and target variable
X_train = data.drop('Bankrupt?', axis=1)
y_train = data['Bankrupt?']

# Train the Random Forest Classifier on the full training data
rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X_train, y_train)

# Make predictions on the test data
predictions = rf_classifier.predict(test_data)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(predictions, columns=["Bankrupt?"])
predictions_df.to_csv('/workspace/bankrupt.csv', index=False)
print("Predictions saved to bankrupt.csv")
