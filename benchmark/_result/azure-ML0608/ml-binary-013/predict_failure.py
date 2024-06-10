import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('/workspace/Train.csv')
test_data = pd.read_csv('/workspace/Test.csv')

# Separate features and target from training data
X_train = train_data.drop('Target', axis=1)
y_train = train_data['Target']

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on test data
predictions = model.predict(test_data)

# Save predictions to CSV
predictions_df = pd.DataFrame(predictions, columns=['Target'])
predictions_df.to_csv('/workspace/target.csv', index=False)
