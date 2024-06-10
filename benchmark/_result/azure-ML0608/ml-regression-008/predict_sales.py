import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Load the datasets
men_shoes = pd.read_csv('vietnamese_tiki_products_men_shoes.csv')
women_shoes = pd.read_csv('vietnamese_tiki_products_women_shoes.csv')
test_data = pd.read_csv('test.csv')

# Combine the datasets
combined_data = pd.concat([men_shoes, women_shoes], ignore_index=True)

# Preprocess the data
# For simplicity, we'll only use numerical features and ignore text and categorical features
features = combined_data[['original_price', 'price', 'review_count', 'rating_average', 'favourite_count', 'number_of_images', 'vnd_cashback']]
target = combined_data['quantity_sold']

# Handle missing values by filling with zero (if any)
features.fillna(0, inplace=True)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(features, target, test_size=0.2, random_state=42)

# Train a RandomForestRegressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred_val = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred_val)
print(f"Validation MSE: {mse}")

# Prepare the test data
test_features = test_data[['original_price', 'price', 'review_count', 'rating_average', 'favourite_count', 'number_of_images', 'vnd_cashback']]
test_features.fillna(0, inplace=True)

# Predict the quantity_sold for the test data
test_data['quantity_sold'] = model.predict(test_features)

# Save the predictions to quantity.csv
test_data[['id', 'quantity_sold']].to_csv('quantity.csv', index=False)
