import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Load the training data
train_data = pd.read_csv('heart.csv')

# Separate features and target
X_train = train_data.drop('output', axis=1)
y_train = train_data['output']

# Preprocess the data: Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess the test data: Scale the features using the same scaler
X_test_scaled = scaler.transform(test_data)

# Make predictions
predictions = model.predict(X_test_scaled)

# Save the predictions to result.csv
result_df = pd.DataFrame(predictions, columns=['output'])
result_df.to_csv('result.csv', index=False)
