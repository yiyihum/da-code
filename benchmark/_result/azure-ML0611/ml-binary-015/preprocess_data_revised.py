import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the datasets
train_data = pd.read_csv('/workspace/clinvar_conflicting.csv', low_memory=False)
test_data = pd.read_csv('/workspace/test.csv', low_memory=False)

# Drop columns with a high percentage of missing values in both training and test sets
columns_to_drop = ['CLNDISDBINCL', 'CLNDNINCL', 'CLNSIGINCL', 'SSR', 'MOTIF_NAME', 'MOTIF_POS', 'HIGH_INF_POS', 'MOTIF_SCORE_CHANGE']
train_data.drop(columns=columns_to_drop, inplace=True)
test_data.drop(columns=columns_to_drop, inplace=True)

# Fill missing values with the mode for categorical columns and mean for numerical columns
for column in train_data.columns:
    if train_data[column].dtype == 'object':
        mode_value = train_data[column].mode()[0]
        train_data[column] = train_data[column].fillna(mode_value)
        test_data[column] = test_data[column].fillna(mode_value)
    else:
        mean_value = train_data[column].mean()
        train_data[column] = train_data[column].fillna(mean_value)
        test_data[column] = test_data[column].fillna(mean_value)

# Encode categorical variables using LabelEncoder
label_encoders = {}
for column in train_data.columns:
    if train_data[column].dtype == 'object':
        le = LabelEncoder()
        # Fit LabelEncoder on the combined data from train and test sets
        le.fit(list(train_data[column].astype(str).values) + list(test_data[column].astype(str).values))
        train_data[column] = le.transform(train_data[column].astype(str).values)
        test_data[column] = le.transform(test_data[column].astype(str).values)
        label_encoders[column] = le

# Save the preprocessed data
train_data.to_csv('/workspace/preprocessed_train.csv', index=False)
test_data.to_csv('/workspace/preprocessed_test.csv', index=False)

# Output the shape of the preprocessed data
print('Preprocessed training data shape:', train_data.shape)
print('Preprocessed test data shape:', test_data.shape)
