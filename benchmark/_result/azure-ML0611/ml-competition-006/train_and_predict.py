import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import cohen_kappa_score

# Load the data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Separate features and target
X = train_data.drop(columns=['Id', 'quality'])
y = train_data['quality']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_val_pred = model.predict(X_val)
val_kappa = cohen_kappa_score(y_val, y_val_pred.round(), weights='quadratic')
print(f"Validation Quadratic Weighted Kappa: {val_kappa}")

# Predict on test data
test_predictions = model.predict(test_data.drop(columns=['Id']))

# Create submission dataframe
submission = pd.DataFrame({
    'Id': test_data['Id'],
    'quality': test_predictions.round()
})

# Save submission file
submission.to_csv('/workspace/submission.csv', index=False)
