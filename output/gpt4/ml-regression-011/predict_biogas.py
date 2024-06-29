import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# Load the training data
train_data = pd.read_csv('veri_seti_son_2.csv')

# Preprocessing: Selecting numerical features and target variable
X = train_data.drop(columns=['Project Name', 'Project Type', 'City', 'County', 'State', 'Digester Type', 'Status', 'Animal/Farm Type(s)', 'Co-Digestion', 'Biogas End Use(s)', 'LCFS Pathway?', 'Receiving Utility', 'Awarded USDA Funding?', 'Biogas Generation Estimate (cu-ft/day)'])
y = train_data['Biogas Generation Estimate (cu-ft/day)']

# Splitting the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating a pipeline with standard scaler and random forest regressor
pipeline = make_pipeline(StandardScaler(), RandomForestRegressor(n_estimators=100, random_state=42))

# Training the model
pipeline.fit(X_train, y_train)

# Validate the model
y_pred_val = pipeline.predict(X_val)
mse = mean_squared_error(y_val, y_pred_val)
print(f"Validation MSE: {mse}")

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocessing: Selecting the same numerical features as the training data
X_test = test_data.drop(columns=['Project Name', 'Project Type', 'City', 'County', 'State', 'Digester Type', 'Status', 'Animal/Farm Type(s)', 'Co-Digestion', 'Biogas End Use(s)', 'LCFS Pathway?', 'Receiving Utility', 'Awarded USDA Funding?'])

# Predicting the biogas generation estimates
test_data['biogas_generation_estimate_cuftday'] = pipeline.predict(X_test)

# Save the predictions to a CSV file
test_data.to_csv('result.csv', index=False, columns=['biogas_generation_estimate_cuftday'])
