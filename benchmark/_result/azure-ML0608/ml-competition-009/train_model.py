import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the training data
train_data = pd.read_csv('train.csv')

# Preprocess the data: convert 'Sex' from categorical to numerical
train_data['Sex'] = train_data['Sex'].map({'M': 0, 'F': 1, 'I': 2})

# Separate features and target
X = train_data.drop(['id', 'Rings'], axis=1)
y = train_data['Rings']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)

# Output the validation error
print(f'Validation RMSE: {rmse}')
