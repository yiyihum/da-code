import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load the training data
train_data = pd.read_csv('train.csv')

# Separate the target variable and the features
y = train_data['yield']
X = train_data.drop(['id', 'yield'], axis=1)

# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=0)

# Create and train the model
model = RandomForestRegressor(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

# Evaluate the model
preds = model.predict(X_valid)
mae = mean_absolute_error(y_valid, preds)
print(f'MAE: {mae}')

# Save the model to a file
joblib.dump(model, 'model.joblib')
