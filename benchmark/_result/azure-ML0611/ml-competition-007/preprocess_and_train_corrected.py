import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
import numpy as np

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Separate target from predictors
y = train_data.SalePrice
X = train_data.drop(['SalePrice'], axis=1)

# Select numerical columns
numerical_cols = [cname for cname in X.columns if X[cname].dtype in ['int64', 'float64']]

# Keep selected columns only
my_cols = numerical_cols
X = X[my_cols].copy()
test_X = test_data[my_cols].copy()

# Split data into training and validation data, for both features and target
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Handle missing values with SimpleImputer
imputer = SimpleImputer()
imputed_X_train = pd.DataFrame(imputer.fit_transform(X_train))
imputed_X_valid = pd.DataFrame(imputer.transform(X_valid))

# Imputation removed column names; put them back
imputed_X_train.columns = X_train.columns
imputed_X_valid.columns = X_valid.columns

# Define the model
model = GradientBoostingRegressor(n_estimators=100, random_state=0)

# Fit the model on the imputed training data
model.fit(imputed_X_train, y_train)

# Get validation predictions and calculate mean squared error
val_predictions = model.predict(imputed_X_valid)
val_mse = mean_squared_error(np.log(y_valid), np.log(val_predictions))
val_rmse = np.sqrt(val_mse)
print("Validation RMSE: ", val_rmse)

# Preprocess the full training data and fit the model
imputed_X = pd.DataFrame(imputer.fit_transform(X))
imputed_X.columns = X.columns
model.fit(imputed_X, y)

# Preprocess test data
final_X_test = pd.DataFrame(imputer.transform(test_X))
final_X_test.columns = test_X.columns

# Generate test predictions
test_preds = model.predict(final_X_test)

# Save test predictions to file
output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})
output.to_csv('/workspace/submission.csv', index=False)
print("Submission file saved.")
