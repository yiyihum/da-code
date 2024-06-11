import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Load the datasets
train_df = pd.read_csv('/workspace/bodyPerformance.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Encode the 'gender' categorical variable
le = LabelEncoder()
train_df['gender'] = le.fit_transform(train_df['gender'])
test_df['gender'] = le.transform(test_df['gender'])

# Split the training data into features and target
X = train_df.drop('class', axis=1)
y = train_df['class']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_classifier.fit(X_train, y_train)

# Validate the model
y_val_pred = rf_classifier.predict(X_val)
val_accuracy = accuracy_score(y_val, y_val_pred)
print(f"Validation Accuracy: {val_accuracy}")

# Make predictions on the test data
test_predictions = rf_classifier.predict(test_df)

# Save the predictions to a CSV file
output = pd.DataFrame({'class': test_predictions})
output.to_csv('/workspace/class.csv', index=False)
