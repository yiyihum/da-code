import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Load the training data
train_data = pd.read_csv('/workspace/data.csv')

# Separate features and target
X_train = train_data.drop(columns=['Bankrupt?'])
y_train = train_data['Bankrupt?']

# Preprocess the data: scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data: scale features using the same scaler as for the training data
X_test_scaled = scaler.transform(test_data)

# Make predictions on the test data
predictions = model.predict(X_test_scaled)

# Write the predictions to a new CSV file
predictions_df = pd.DataFrame(predictions, columns=['Bankrupt?'])
predictions_df.to_csv('/workspace/bankrupt.csv', index=False)
