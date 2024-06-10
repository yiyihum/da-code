import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Load the datasets
historical_data = pd.read_csv('top_10000_1960-now.csv')
test_data = pd.read_csv('test.csv')

# Drop columns with all missing values
historical_data = historical_data.dropna(axis=1, how='all')
test_data = test_data.dropna(axis=1, how='all')

# Preprocessing
# Impute missing values with the mean for numerical columns and the most frequent value for categorical columns
numerical_cols = historical_data.select_dtypes(include=['float64', 'int']).columns
numerical_cols = numerical_cols.drop('Popularity')  # Exclude the target variable
categorical_cols = historical_data.select_dtypes(include=['object']).columns

# Impute missing values
imputer_num = SimpleImputer(strategy='mean')
imputer_cat = SimpleImputer(strategy='most_frequent')

historical_data[numerical_cols] = imputer_num.fit_transform(historical_data[numerical_cols])
historical_data[categorical_cols] = imputer_cat.fit_transform(historical_data[categorical_cols])

test_data[numerical_cols] = imputer_num.transform(test_data[numerical_cols])
test_data[categorical_cols] = imputer_cat.transform(test_data[categorical_cols])

# We will not use the non-numeric columns for the prediction model
X = historical_data.drop(categorical_cols, axis=1)
X = X.drop('Popularity', axis=1)
y = historical_data['Popularity']

# Split the historical data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Ensure we only select the numerical columns that were used to fit the scaler
test_data_scaled = scaler.transform(test_data[X_train.columns])

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Validate the model
y_pred_val = model.predict(X_val_scaled)
mse = mean_squared_error(y_val, y_pred_val)
print(f"Validation MSE: {mse}")

# Predict on test data
test_predictions = model.predict(test_data_scaled)

# Save the predictions to a CSV file
test_data['Popularity'] = test_predictions
test_data[['Track URI', 'Popularity']].to_csv('popularity.csv', index=False)
print("Predictions saved to popularity.csv")
