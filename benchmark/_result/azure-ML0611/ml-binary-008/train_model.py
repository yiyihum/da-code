import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the preprocessed training and validation data
X_train = pd.read_csv('/workspace/X_train.csv')
y_train = pd.read_csv('/workspace/y_train.csv')
X_valid = pd.read_csv('/workspace/X_valid.csv')
y_valid = pd.read_csv('/workspace/y_valid.csv')

# Train a logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train.values.ravel())

# Validate the model
y_pred = model.predict(X_valid)
accuracy = accuracy_score(y_valid, y_pred)
print(f"Validation accuracy: {accuracy}")

# Save the trained model for later use
with open('/workspace/logistic_regression_model.pkl', 'wb') as file:
    pickle.dump(model, file)
