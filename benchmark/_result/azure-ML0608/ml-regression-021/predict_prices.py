import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Function to convert mileage, engine, and power to numeric values
def extract_numeric(value):
    try:
        if isinstance(value, str):
            value = value.lower().strip()
            if 'null' in value or value == '':
                return np.nan
            return float(value.split()[0])
        return value
    except ValueError as e:
        print(f"Error converting value: {value}")
        return np.nan

# Load the training data
train_data = pd.read_csv('/workspace/train-data.csv')

# Preprocessing
# Dropping the 'Unnamed: 0' and 'Name' columns as they are not needed for prediction
train_data.drop(columns=['Unnamed: 0', 'Name', 'New_Price'], inplace=True)

# Convert 'Mileage', 'Engine', and 'Power' to numeric values after removing units
train_data['Mileage'] = train_data['Mileage'].apply(extract_numeric)
train_data['Engine'] = train_data['Engine'].apply(extract_numeric)
train_data['Power'] = train_data['Power'].apply(extract_numeric)

# Convert categorical variables to numeric
label_encoders = {}
for column in ['Location', 'Fuel_Type', 'Transmission', 'Owner_Type']:
    le = LabelEncoder()
    train_data[column] = le.fit_transform(train_data[column].astype(str))
    label_encoders[column] = le

# Ensure all numeric columns are of type float
numeric_columns = ['Year', 'Kilometers_Driven', 'Mileage', 'Engine', 'Power', 'Seats']
train_data[numeric_columns] = train_data[numeric_columns].astype(float)

# Fill missing values with the mean value for numerical columns
train_data.fillna(train_data.mean(), inplace=True)

# Splitting the data into features and target
X = train_data.drop(columns=['Price'])
y = train_data['Price']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f'Mean Squared Error on validation set: {mse}')

# Load the test data
test_data = pd.read_csv('/workspace/test-data.csv')
test_data.drop(columns=['Unnamed: 0', 'Name', 'New_Price'], inplace=True)  # Drop 'Name' and 'New_Price' columns

# Apply the same preprocessing to the test data
test_data['Mileage'] = test_data['Mileage'].apply(extract_numeric)
test_data['Engine'] = test_data['Engine'].apply(extract_numeric)
test_data['Power'] = test_data['Power'].apply(extract_numeric)

# Transform categorical variables using the label encoders
for column, le in label_encoders.items():
    test_data[column] = le.transform(test_data[column].astype(str))

# Ensure all numeric columns are of type float
test_data[numeric_columns] = test_data[numeric_columns].astype(float)

# Fill missing values with the mean value for numerical columns
test_data.fillna(test_data.mean(), inplace=True)

# Predict the prices for the test data
test_data['Price'] = model.predict(test_data)

# Save the predicted prices to a CSV file
test_data[['Price']].to_csv('/workspace/price.csv', index=False)
