import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load the training data
train_data = pd.read_csv('/workspace/drugsComTrain_raw.csv')

# Drop the 'Unnamed: 0' and 'date' columns as they are not useful for prediction
train_data = train_data.drop(['Unnamed: 0', 'date'], axis=1)

# Handle missing values in 'condition' by replacing them with a placeholder string
train_data['condition'].fillna('Unknown', inplace=True)

# Select features and target variable for the model
X = train_data[['rating']]  # Using only 'rating' for simplicity
y = train_data['usefulCount']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the random forest regressor
regressor = RandomForestRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train, y_train)

# Predict on the validation set
y_pred = regressor.predict(X_val)

# Calculate the mean squared error on the validation set
mse = mean_squared_error(y_val, y_pred)
print(f'Mean Squared Error: {mse}')
