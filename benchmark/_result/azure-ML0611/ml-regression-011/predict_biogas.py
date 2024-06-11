import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline

# Load the training data
train_data = pd.read_csv('veri_seti_son_2.csv')

# Preprocessing: Drop non-relevant columns for simplicity
columns_to_drop = ['Project Name', 'City', 'County', 'State', 'Digester Type', 'Status',
                   'Animal/Farm Type(s)', 'Biogas End Use(s)', 'LCFS Pathway?', 'Receiving Utility',
                   'Awarded USDA Funding?']
train_data = train_data.drop(columns=columns_to_drop)

# Replace 'No-Info' with NaN and drop rows with NaN values
train_data = train_data.replace('No-Info', pd.NA)
train_data = train_data.dropna()

# Identify categorical columns (assuming 'No-Info' is a placeholder for missing categorical data)
categorical_cols = train_data.select_dtypes(include=['object']).columns.tolist()

# Separate features and target
X = train_data.drop('Biogas Generation Estimate (cu-ft/day)', axis=1)
y = train_data['Biogas Generation Estimate (cu-ft/day)']

# Define a transformer for the categorical columns
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Create a preprocessor that will one-hot encode categorical columns
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_cols)
    ],
    remainder='passthrough'  # Passthrough numerical columns as is
)

# Create a pipeline with the preprocessor and a RandomForestRegressor
pipeline = make_pipeline(preprocessor, StandardScaler(with_mean=False), RandomForestRegressor(n_estimators=100, random_state=42))

# Train the model
pipeline.fit(X, y)

# Load the test data
test_data = pd.read_csv('test.csv')
test_data = test_data.drop(columns=columns_to_drop)
test_data = test_data.replace('No-Info', pd.NA)
test_data = test_data.fillna(0)  # Assuming missing values can be filled with 0

# Predict on the test data
test_predictions = pipeline.predict(test_data)

# Save the predictions to a CSV file
result = pd.DataFrame(test_predictions, columns=['biogas_generation_estimate_cuftday'])
result.to_csv('result.csv', index=False)
