import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('/workspace/activities.csv')

# Assuming the last column is the target variable
X_train = train_data.iloc[:, :-1]
y_train = train_data.iloc[:, -1]

# Load the test data
test_data = pd.read_csv('/workspace/activity_test.csv')

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict the activities
predictions = model.predict(test_data)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(predictions, columns=['Activity'])
predictions_df.to_csv('/workspace/activity.csv', index=False)
