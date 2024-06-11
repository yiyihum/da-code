import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OrdinalEncoder

# Load the training data
train_data = pd.read_csv('/workspace/train-data.csv')

# Preprocessing
def preprocess_data(data, fit_encoders=False):
    # Drop the 'Unnamed: 0' and 'New_Price' columns as they are not useful for training
    data = data.drop(['Unnamed: 0', 'New_Price'], axis=1)
    
    # Extract numerical values from the columns with units and convert to float
    for column in ['Mileage', 'Engine', 'Power']:
        data[column] = data[column].str.extract('(\d+\.?\d*)').astype(float)
    
    # Fill missing values with the mean value for numerical columns
    data['Seats'] = data['Seats'].fillna(data['Seats'].mean())
    
    # Convert categorical variables to numeric using ordinal encoding
    categorical_columns = ['Name', 'Location', 'Fuel_Type', 'Transmission', 'Owner_Type']
    if fit_encoders:
        global ordinal_encoder
        ordinal_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        data[categorical_columns] = ordinal_encoder.fit_transform(data[categorical_columns])
    else:
        data[categorical_columns] = ordinal_encoder.transform(data[categorical_columns])
    
    return data

# Preprocess the training data and fit the encoders
train_data = preprocess_data(train_data, fit_encoders=True)

# Split the data into features and target variable
X = train_data.drop('Price', axis=1)
y = train_data['Price']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f'Mean Squared Error: {mse}')

# Load the test data
test_data = pd.read_csv('/workspace/test-data.csv')

# Preprocess the test data without fitting the encoders (use the fitted encoders from the training data)
test_data = preprocess_data(test_data)

# Predict the prices for the test data
test_data['Price'] = model.predict(test_data)

# Save the predicted prices to a CSV file
test_data[['Price']].to_csv('/workspace/price.csv', index=False)
