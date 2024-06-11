import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer

# Load the historical data
historical_data = pd.read_csv('/workspace/data.csv')

# Preprocess the data
# Select only numerical columns excluding the target variable
numerical_columns = historical_data.select_dtypes(include=['float64', 'int64']).columns.drop('AVG_JOB_SATISFACTION')

# Impute missing values for all numerical columns with the mean
imputer = SimpleImputer(strategy='mean')
historical_data[numerical_columns] = imputer.fit_transform(historical_data[numerical_columns])

# Separate features and target variable
X = historical_data.drop(columns=['GEO', 'COUNTRY', 'AVG_JOB_SATISFACTION'])
y = historical_data['AVG_JOB_SATISFACTION']

# Train a linear regression model
model = LinearRegression()
model.fit(X, y)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data
# Apply the same imputation to the test data
test_data[numerical_columns] = imputer.transform(test_data[numerical_columns])

# Predict the 'AVG_JOB_SATISFACTION' for the test data
test_data['AVG_JOB_SATISFACTION'] = model.predict(test_data.drop(columns=['GEO', 'COUNTRY']))

# Save the predictions to a new CSV file
test_data[['AVG_JOB_SATISFACTION']].to_csv('/workspace/job_satisfaction.csv', index=False)
