import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the data
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# Perform exploratory data analysis
print(train.head())
print(test.head())

# Preprocess the data
train = train.select_dtypes(include=[np.number]).interpolate().dropna()
test = test.select_dtypes(include=[np.number]).interpolate().dropna()

# Split the data into features and target variable
y = np.log(train.SalePrice)
X = train.drop(['SalePrice', 'Id'], axis=1)

# Split the data into training and validation sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=.33)

# Train a model
model = RandomForestRegressor(n_estimators=1000)
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Calculate RMSE
print('RMSE:', np.sqrt(mean_squared_error(y_test, predictions)))

# Make predictions for the test set
final_predictions = np.exp(model.predict(test.drop(['Id'], axis=1)))

# Write the predictions into the submission.csv file
submission = pd.DataFrame()
submission['Id'] = test.Id
submission['SalePrice'] = final_predictions
submission.to_csv('submission.csv', index=False)
