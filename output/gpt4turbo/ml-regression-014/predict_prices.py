import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the datasets
train_data = pd.read_csv('Car_Prices_Poland_Kaggle.csv')
test_data = pd.read_csv('test.csv')

# Preprocessing
# Drop the 'Unnamed: 0' column as it's just an index
train_data.drop(columns=['Unnamed: 0'], inplace=True)
test_data.drop(columns=['Unnamed: 0'], inplace=True)

# For simplicity, let's drop rows with any missing values and non-numeric columns
train_data.dropna(inplace=True)
test_data.dropna(inplace=True)
train_data = train_data.select_dtypes(include=[np.number])
test_data = test_data.select_dtypes(include=[np.number])

# Split the training data into features and target
X_train = train_data.drop(columns=['price'])
y_train = train_data['price']

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict the prices for the test data
X_test = test_data
predicted_prices = model.predict(X_test)

# Save the predicted prices to a CSV file
predicted_prices_df = pd.DataFrame(predicted_prices, columns=['price'])
predicted_prices_df.to_csv('price.csv', index=False)
