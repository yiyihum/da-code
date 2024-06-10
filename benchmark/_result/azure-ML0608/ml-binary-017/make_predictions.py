import pandas as pd
from sklearn.impute import SimpleImputer
import joblib

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess the test data
# Select numerical columns
numerical_cols = test_data.select_dtypes(exclude=['object']).columns

# Imputation
imputer = SimpleImputer()
imputed_test_data = pd.DataFrame(imputer.fit_transform(test_data[numerical_cols]))

# Imputation removed column names; put them back
imputed_test_data.columns = numerical_cols

# Load the trained model
model = joblib.load('rain_model.joblib')

# Make predictions on the test data
predictions = model.predict(imputed_test_data)

# Save the predictions to a CSV file
output = pd.DataFrame({'RainTomorrow': predictions})
output.to_csv('tomorrow.csv', index=False)
