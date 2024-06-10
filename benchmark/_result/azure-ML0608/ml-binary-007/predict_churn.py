import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('customer_churn_dataset-training-master.csv')

# Drop rows with NaN values in the 'Churn' column
train_data = train_data.dropna(subset=['Churn'])

# Load the testing data
test_data = pd.read_csv('customer_churn_dataset-testing-master.csv')

# Combine the training and testing data to fit the label encoder
combined_data = pd.concat([train_data.drop(columns=['Churn']), test_data], axis=0)

# Preprocess the data: encode categorical variables
label_encoder = LabelEncoder()
categorical_columns = combined_data.select_dtypes(include=['object']).columns
for column in categorical_columns:
    # Fit the label encoder on the combined data
    combined_unique = combined_data[column].astype(str).unique()
    label_encoder.fit(combined_unique)
    # Transform both training and testing data
    train_data[column] = label_encoder.transform(train_data[column].astype(str))
    test_data[column] = label_encoder.transform(test_data[column].astype(str))

# Exclude 'CustomerID' from the features
X_train = train_data.drop(columns=['Churn', 'CustomerID'])
y_train = train_data['Churn']
X_test = test_data.drop(columns=['CustomerID'])

# Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict churn for the testing data
predictions = model.predict(X_test)

# Write the prediction results into result.csv with the column name 'result'
result_df = pd.DataFrame(predictions, columns=['result'])
result_df.to_csv('result.csv', index=False)
