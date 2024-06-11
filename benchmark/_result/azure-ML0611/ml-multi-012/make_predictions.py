import pandas as pd
import joblib

# Load the incomplete data
incomplete_data = pd.read_csv('/workspace/incomplete_info.csv')

# Keep the building_id for the output file
building_ids = incomplete_data['building_id']

# Drop the building_id from the features as it's not used for prediction
incomplete_data = incomplete_data.drop(columns=['building_id'])

# Convert categorical variables to dummy variables
incomplete_data = pd.get_dummies(incomplete_data)

# Load the trained model
rf_model = joblib.load('/workspace/rf_model.joblib')

# Ensure that the columns of the incomplete data match those of the training data
# This is necessary because the dummy variable may have different columns
missing_cols = set(rf_model.feature_names_in_) - set(incomplete_data.columns)
for c in missing_cols:
    incomplete_data[c] = 0
incomplete_data = incomplete_data[rf_model.feature_names_in_]

# Predict the damage grade
predicted_damage_grade = rf_model.predict(incomplete_data)

# Create a DataFrame with the building_id and the predicted damage_grade
predictions = pd.DataFrame({
    'building_id': building_ids,
    'damage_grade': predicted_damage_grade
})

# Save the predictions to a CSV file
predictions.to_csv('/workspace/prediction.csv', index=False)
