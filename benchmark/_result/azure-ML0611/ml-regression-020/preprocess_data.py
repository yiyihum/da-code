import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Preprocessing steps:
# 1. Handle missing values
# 2. Convert categorical variables to numerical
# 3. Create new features if necessary

# Fill missing values with the mean for numerical columns and the mode for categorical columns
for column in train_data.columns:
    if column not in ['ID', 'Time_taken(min)']:  # Exclude ID and target column
        if train_data[column].dtype == 'object':  # Categorical
            mode_value = train_data[column].mode()[0]
            train_data[column] = train_data[column].fillna(mode_value)
            test_data[column] = test_data[column].fillna(mode_value)
        else:  # Numerical
            mean_value = train_data[column].mean()
            train_data[column] = train_data[column].fillna(mean_value)
            test_data[column] = test_data[column].fillna(mean_value)

# Encode categorical variables using LabelEncoder
label_encoders = {}
categorical_columns = train_data.select_dtypes(include=['object']).columns.drop('ID')
for column in categorical_columns:
    le = LabelEncoder()
    le.fit(train_data[column])
    train_data[column] = le.transform(train_data[column])
    test_data[column] = le.transform(test_data[column])
    label_encoders[column] = le

# Split the training data into features and target variable
X = train_data.drop(columns=['Time_taken(min)', 'ID'])
y = train_data['Time_taken(min)']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the preprocessed data and the label encoders for later use
X_train.to_csv('/workspace/X_train.csv', index=False)
y_train.to_csv('/workspace/y_train.csv', index=False)
X_val.to_csv('/workspace/X_val.csv', index=False)
y_val.to_csv('/workspace/y_val.csv', index=False)
test_data.to_csv('/workspace/test_preprocessed.csv', index=False)

# Output the shape of the datasets as a sanity check
print(f"Training features shape: {X_train.shape}")
print(f"Training target shape: {y_train.shape}")
print(f"Validation features shape: {X_val.shape}")
print(f"Validation target shape: {y_val.shape}")
print(f"Test features shape: {test_data.shape}")
