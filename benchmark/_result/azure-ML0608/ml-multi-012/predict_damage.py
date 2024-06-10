import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

# Load the complete dataset
complete_data = pd.read_csv('/workspace/complete_info.csv')

# Identify categorical columns
categorical_cols = complete_data.select_dtypes(include=['object']).columns

# One-hot encode the categorical columns
encoder = OneHotEncoder(handle_unknown='ignore')
encoded_features = encoder.fit_transform(complete_data[categorical_cols]).toarray()

# Create a DataFrame with the encoded features
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_cols))

# Drop the original categorical columns and concatenate the encoded features
complete_data = complete_data.drop(columns=categorical_cols)
complete_data = pd.concat([complete_data.reset_index(drop=True), encoded_df], axis=1)

# Exclude 'building_id' from the features
X = complete_data.drop(columns=['damage_grade', 'building_id'])
y = complete_data['damage_grade']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")

# Load the incomplete dataset
incomplete_data = pd.read_csv('/workspace/incomplete_info.csv')

# One-hot encode the categorical columns in the incomplete dataset using the same encoder
incomplete_encoded_features = encoder.transform(incomplete_data[categorical_cols]).toarray()
incomplete_encoded_df = pd.DataFrame(incomplete_encoded_features, columns=encoder.get_feature_names_out(categorical_cols))

# Drop the original categorical columns and concatenate the encoded features
incomplete_data = incomplete_data.drop(columns=categorical_cols)
incomplete_data = pd.concat([incomplete_data.reset_index(drop=True), incomplete_encoded_df], axis=1)

# Predict the damage grades for the incomplete dataset
predictions = model.predict(incomplete_data.drop(columns=['building_id']))

# Save the predictions to a CSV file
prediction_df = incomplete_data[['building_id']].copy()
prediction_df['damage_grade'] = predictions
prediction_df.to_csv('/workspace/prediction.csv', index=False)
