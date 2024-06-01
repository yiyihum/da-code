import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('train.csv')
X_train = train_data.drop(['id', 'Unnamed: 32', 'diagnosis'], axis=1)
y_train = train_data['diagnosis']

# Load the test data
test_data = pd.read_csv('test.csv')
X_test = test_data.drop(['id', 'Unnamed: 32'], axis=1)

# Train the Random Forest Classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train, y_train)

# Predict on the test data
predictions = classifier.predict(X_test)

# Write predictions to label.csv
predictions_df = pd.DataFrame(predictions, columns=['result'])
predictions_df.to_csv('label.csv', index=False)
