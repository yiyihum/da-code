import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Load datasets
energy_data = pd.read_csv('/workspace/energy_dataset.csv')
weather_data = pd.read_csv('/workspace/weather_features.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Convert time columns to datetime
energy_data['time'] = pd.to_datetime(energy_data['time'], utc=True)
weather_data['dt_iso'] = pd.to_datetime(weather_data['dt_iso'], utc=True)
test_data['time'] = pd.to_datetime(test_data['time'], utc=True)

# Encode categorical variables in weather data
label_encoder = LabelEncoder()
weather_data['city_name_encoded'] = label_encoder.fit_transform(weather_data['city_name'])

# Merge datasets on the time column
merged_data = pd.merge(energy_data, weather_data, left_on='time', right_on='dt_iso')

# Drop unnecessary columns
columns_to_drop = ['time', 'dt_iso', 'weather_id', 'weather_icon', 'weather_description', 'weather_main', 'city_name']
merged_data.drop(columns=columns_to_drop, inplace=True)

# Handle missing values for numeric columns only
numeric_columns = merged_data.select_dtypes(include=[np.number]).columns
merged_data[numeric_columns] = merged_data[numeric_columns].fillna(merged_data[numeric_columns].mean())

# Prepare features and target variable
X = merged_data.drop('price actual', axis=1)
y = merged_data['price actual']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Validate the model
y_pred = rf.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)
print(f'Validation RMSE: {rmse}')

# Save the trained model to a file
import joblib
joblib.dump(rf, '/workspace/electricity_price_predictor.joblib')
