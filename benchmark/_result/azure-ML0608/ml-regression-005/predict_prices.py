import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Remove rows with non-numeric 'price' values
train_data = train_data[pd.to_numeric(train_data['price'], errors='coerce').notnull()]

# Select a subset of features that are likely to be numeric and non-categorical
selected_features = ['year', 'mileage', 'engine_size', 'min_mpg', 'max_mpg']

# Separate features and target
X_train = train_data[selected_features]
y_train = train_data['price'].astype(float)

# Fill missing values for numeric columns with the mean of the column
X_train = X_train.fillna(X_train.mean())

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data using the same selected features
X_test = test_data[selected_features]
X_test = X_test.fillna(X_train.mean())

# Initialize the LinearRegression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Predict the prices on the test data
predictions = model.predict(X_test)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(predictions, columns=['price'])
predictions_df.to_csv('/workspace/price.csv', index=False)
