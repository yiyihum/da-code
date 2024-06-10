import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Function to clean the price column
def clean_price(price):
    if isinstance(price, str):
        return float(price.replace('$', '').replace(',', ''))
    return price

# Function to count the number of amenities
def count_amenities(amenities):
    if isinstance(amenities, str):
        amenities = amenities.strip("[]").replace("'", "").split(', ')
        return len(amenities)
    return 0

# Load the cleaned dataset to train the model
cleaned_data = pd.read_csv('/workspace/Cleaned_airbnb_barcelona.csv')

# Clean the 'price' column
cleaned_data['price'] = cleaned_data['price'].apply(clean_price)

# Count the number of amenities
cleaned_data['amenities_count'] = cleaned_data['amenities'].apply(count_amenities)

# Drop the original 'amenities' column
cleaned_data.drop('amenities', axis=1, inplace=True)

# Preprocessing: Convert categorical variables to dummy variables
categorical_features = ['host_is_superhost', 'neighbourhood', 'property_type', 'room_type', 'has_availability', 'zipcode']
cleaned_data = pd.get_dummies(cleaned_data, columns=categorical_features)

# Selecting relevant features for the model
# Assuming that the test set has the same feature set as the cleaned data
features = [col for col in cleaned_data.columns if col != 'price']
target = 'price'

# Split the data into features and target
X = cleaned_data[features]
y = cleaned_data[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate the mean squared error
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Load the test dataset to predict the prices
test_data = pd.read_csv('/workspace/test.csv')

# Count the number of amenities for the test data
test_data['amenities_count'] = test_data['amenities'].apply(count_amenities)

# Drop the original 'amenities' column from the test data
test_data.drop('amenities', axis=1, inplace=True)

# Preprocessing: Convert categorical variables to dummy variables
test_data = pd.get_dummies(test_data, columns=categorical_features)

# Ensure the test data has the same dummy variable columns as the training data
test_data = test_data.reindex(columns=X.columns, fill_value=0)

# Predict the prices for the test dataset
test_prices = model.predict(test_data[features])

# Create a DataFrame with the predicted prices
price_df = pd.DataFrame(test_prices, columns=['price'])

# Save the predicted prices to a CSV file
price_df.to_csv('/workspace/price.csv', index=False)
