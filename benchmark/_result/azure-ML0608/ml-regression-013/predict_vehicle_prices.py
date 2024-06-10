import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the training data
train_data = pd.read_csv('Car details v3.csv')

# Selecting relevant columns for training and prediction
features = ['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner']
target = 'selling_price'

# Preprocessing the categorical data with OneHotEncoder and handle_unknown='ignore' to ignore new categories
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Preprocessor for the pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, ['fuel', 'seller_type', 'transmission', 'owner'])
    ],
    remainder='passthrough'
)

# Create the model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    train_data[features], train_data[target], test_size=0.2, random_state=0
)

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Load the test data
test_data = pd.read_csv('test.csv')

# Rename columns in the test data to match the training data
test_data.rename(columns={
    'Year': 'year',
    'Kms_Driven': 'km_driven',
    'Fuel_Type': 'fuel',
    'Seller_Type': 'seller_type',
    'Transmission': 'transmission',
    'Owner': 'owner'
}, inplace=True)

# Predict the selling prices using the model
predicted_prices = model.predict(test_data[features])

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(predicted_prices, columns=["Selling_Price"])
predictions_df.to_csv('price.csv', index=False)
