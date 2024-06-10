import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import numpy as np

# Function to calculate SMAPE
def smape(A, F):
    return 100/len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))

# Load the merged training data
train_merged_df = pd.read_csv('/workspace/train_merged.csv')

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Load the additional census data
census_df = pd.read_csv('/workspace/census_starter.csv')

# Merge the test data with the census data on the 'cfips' column
test_merged_df = pd.merge(test_df, census_df, on='cfips', how='left')

# Select a subset of features for simplicity
selected_features = ['active', 'pct_bb_2021', 'pct_college_2021', 'pct_foreign_born_2021', 'pct_it_workers_2021', 'median_hh_inc_2021']

# Preprocessing: Use only selected features
X = train_merged_df[selected_features]
y = train_merged_df['microbusiness_density']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Impute missing values with median
imputer = SimpleImputer(strategy='median')
X_train_imputed = imputer.fit_transform(X_train)
X_val_imputed = imputer.transform(X_val)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_val_scaled = scaler.transform(X_val_imputed)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Predict on the validation set
y_val_pred = model.predict(X_val_scaled)

# Calculate SMAPE on the validation set
validation_smape = smape(y_val, y_val_pred)
print(f'Validation SMAPE: {validation_smape}')

# Prepare the test set for prediction
X_test = test_merged_df[selected_features]
X_test_imputed = imputer.transform(X_test)
X_test_scaled = scaler.transform(X_test_imputed)

# Predict on the test set
test_predictions = model.predict(X_test_scaled)

# Create the submission file
submission_df = pd.DataFrame({
    'row_id': test_df['row_id'],
    'microbusiness_density': test_predictions
})
submission_df.to_csv('/workspace/submission.csv', index=False)
print('Submission file created.')
