import pandas as pd
from sklearn.model_selection import train_test_split
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
        train_data[column].fillna(train_data[column].mode()[0], inplace=True)
        test_data[column].fillna(train_data[column].mode()[0], inplace=True)
    else:
        train_data[column].fillna(train_data[column].mean(), inplace=True)
        test_data[column].fillna(train_data[column].mean(), inplace=True)

# Encode categorical variables using LabelEncoder
label_encoders = {}
for column in train_data.columns:
    if train_data[column].dtype == 'object':
        le = LabelEncoder()
        train_data[column] = le.fit_transform(train_data[column])
        test_data[column] = le.transform(test_data[column])
        label_encoders[column] = le

# Save the preprocessed data
train_data.to_csv('/workspace/preprocessed_train.csv', index=False)
test_data.to_csv('/workspace/preprocessed_test.csv', index=False)

# Output the shape of the preprocessed data
print('Preprocessed training data shape:', train_data.shape)
print('Preprocessed test data shape:', test_data.shape)
