import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X = train_data.drop(columns=['ID_LAT_LON_YEAR_WEEK', 'emission'])
y = train_data['emission']

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# Initialize the model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f"Validation MSE: {mse}")

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Prepare test features and impute missing values
X_test = test_data.drop(columns=['ID_LAT_LON_YEAR_WEEK'])
X_test_imputed = imputer.transform(X_test)

# Make predictions on the test data
test_predictions = model.predict(X_test_imputed)

# Create a submission dataframe
submission = pd.DataFrame({
    'ID_LAT_LON_YEAR_WEEK': test_data['ID_LAT_LON_YEAR_WEEK'],
    'emission': test_predictions
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
