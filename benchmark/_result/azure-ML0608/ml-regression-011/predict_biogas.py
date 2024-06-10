import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Function to handle unseen labels during label encoding
def encode_with_unseen_labels(train_series, test_series):
    le = LabelEncoder()
    le.fit(list(train_series.astype(str)) + list(test_series.astype(str)))
    return le.transform(train_series.astype(str)), le.transform(test_series.astype(str))

# Load the training data
train_data = pd.read_csv('veri_seti_son_2.csv')

# Preprocess the data
# For simplicity, let's drop rows with missing target values
train_data.dropna(subset=['Biogas Generation Estimate (cu-ft/day)'], inplace=True)

# Load the test data
test_data = pd.read_csv('test.csv')

# Encode categorical variables with the function that handles unseen labels
categorical_cols = train_data.select_dtypes(include=['object']).columns
for col in categorical_cols:
    train_data[col], test_data[col] = encode_with_unseen_labels(train_data[col], test_data[col])

# Separate features and target
X_train = train_data.drop('Biogas Generation Estimate (cu-ft/day)', axis=1)
y_train = train_data['Biogas Generation Estimate (cu-ft/day)']

# Train a regression model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict the 'Biogas Generation Estimate (cu-ft/day)' for the test data
X_test = test_data.drop('Biogas Generation Estimate (cu-ft/day)', axis=1, errors='ignore')
predictions = model.predict(X_test)

# Save the predictions in a new CSV file
result = pd.DataFrame(predictions, columns=['biogas_generation_estimate_cuftday'])
result.to_csv('result.csv', index=False)
