import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# Load the preprocessed and merged dataset
merged_data = pd.read_csv('/workspace/merged_data.csv', index_col=0)

# Load the test dataset and weather dataset
test_data = pd.read_csv('/workspace/test.csv')
weather_data = pd.read_csv('/workspace/weather_features.csv')

# Convert the 'time' columns to datetime objects and localize to UTC
test_data['time'] = pd.to_datetime(test_data['time'], utc=True)
weather_data['dt_iso'] = pd.to_datetime(weather_data['dt_iso'], utc=True)

# Set the 'time' columns as the index
test_data.set_index('time', inplace=True)
weather_data.set_index('dt_iso', inplace=True)

# Merge the test data with the weather data on the datetime index
test_data_merged = pd.merge(test_data, weather_data, left_index=True, right_index=True, how='left')

# Drop non-numeric columns that are not needed for prediction
non_numeric_cols = ['city_name', 'weather_icon', 'weather_id', 'weather_description', 'weather_main']
test_data_merged.drop(columns=non_numeric_cols, inplace=True)

# Separate the target variable and features
X = merged_data.drop(columns=['price actual'])
y = merged_data['price actual']

# Impute missing values with the mean for the training data
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# Initialize a Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f'Mean Squared Error: {mse}')

# Impute missing values in the test data
test_data_imputed = imputer.transform(test_data_merged)

# Predict the 'price actual' for the test set
test_predictions = model.predict(test_data_imputed)

# Save the predictions to a CSV file
prediction_df = pd.DataFrame(test_predictions, columns=['price actual'])
prediction_df.to_csv('/workspace/result.csv', index=False)

print('Prediction complete. Results saved to /workspace/result.csv')
