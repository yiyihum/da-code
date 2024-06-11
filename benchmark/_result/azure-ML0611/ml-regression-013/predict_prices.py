import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the training dataset
train_data = pd.read_csv('/workspace/car data.csv')

# Preprocessing
# Dropping the 'Car_Name' column as it's likely not useful for the model
train_data = train_data.drop('Car_Name', axis=1)

# Separating the features and target variable for training data
X_train = train_data.drop('Selling_Price', axis=1)
y_train = train_data['Selling_Price']

# Handling categorical variables with one-hot encoding
categorical_features = ['Fuel_Type', 'Seller_Type', 'Transmission', 'Owner']
one_hot_encoder = OneHotEncoder()

# Creating a column transformer to transform categorical features
preprocessor = ColumnTransformer(transformers=[
    ('cat', one_hot_encoder, categorical_features)
], remainder='passthrough')

# Creating a pipeline that first transforms the data and then applies linear regression
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Fitting the model with the training data
model.fit(X_train, y_train)

# Load the test dataset
test_data = pd.read_csv('/workspace/test.csv')
test_data = test_data.drop('Car_Name', axis=1)  # Consistent with training data preprocessing

# Predicting the selling prices for the test dataset
predicted_prices = model.predict(test_data)

# Saving the predicted selling prices into a file named "price.csv" with the column name "Selling_Price"
predicted_prices_df = pd.DataFrame(predicted_prices, columns=['Selling_Price'])
predicted_prices_df.to_csv('/workspace/price.csv', index=False)
