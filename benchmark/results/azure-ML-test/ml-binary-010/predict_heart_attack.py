import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load the training data
train_data = pd.read_csv('heart.csv')

# Split the data into features and target
X_train = train_data.drop('output', axis=1)
y_train = train_data['output']

# Preprocess the data: Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess the test data with the same scaler
X_test = scaler.transform(test_data)

# Make predictions
predictions = model.predict(X_test)

# Write the predictions to a CSV file
result = pd.DataFrame(predictions, columns=['output'])
result.to_csv('result.csv', index=False)