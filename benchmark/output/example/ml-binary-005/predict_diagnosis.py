import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load and preprocess the training data
train_data = pd.read_csv('train.csv')
train_data.drop(columns=['id', 'Unnamed: 32'], inplace=True)
X_train = train_data.drop(columns=['diagnosis'])
y_train = train_data['diagnosis']

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Load and preprocess the test data
test_data = pd.read_csv('test.csv')
test_ids = test_data['id']
test_data.drop(columns=['id', 'Unnamed: 32'], inplace=True)

# Predict the diagnosis for the test data
predictions = model.predict(test_data)

# Output the predictions to a CSV file
results = pd.DataFrame({'id': test_ids, 'result': predictions})
results.to_csv('label.csv', index=False, header=True)