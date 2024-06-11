import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Separate the ID and features
test_ids = test_data['ID_LAT_LON_YEAR_WEEK']
test_features = test_data.drop(columns=['ID_LAT_LON_YEAR_WEEK'])

# Define a pipeline with an imputer for missing values and a random forest regressor
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values with the mean
    ('scaler', StandardScaler()),  # Scale features
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))  # Random forest regressor
])

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')
train_features = train_data.drop(columns=['ID_LAT_LON_YEAR_WEEK', 'emission'])
train_targets = train_data['emission']

# Fit the pipeline to the training data
pipeline.fit(train_features, train_targets)

# Predict on the test data
test_predictions = pipeline.predict(test_features)

# Create the submission DataFrame
submission = pd.DataFrame({
    'ID_LAT_LON_YEAR_WEEK': test_ids,
    'emission': test_predictions
})

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
