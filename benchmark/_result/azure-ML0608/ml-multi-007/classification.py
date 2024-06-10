import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the datasets
train_data = pd.read_csv('Date_Fruit_Datasets.csv')
test_data = pd.read_csv('test.csv')

# Separate features and target variable
X_train = train_data.drop('Class', axis=1)
y_train = train_data['Class']
X_test = test_data

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict the classes for the test set
predictions = model.predict(X_test)

# Save the predictions to a CSV file
output = pd.DataFrame({'Class': predictions})
output.to_csv('class.csv', index=False)
