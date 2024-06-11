import pandas as pd

# Re-merge the datasets since the previous merged dataframes are not saved as CSV files
train = pd.read_csv('/workspace/train.csv')
test = pd.read_csv('/workspace/test.csv')
stores = pd.read_csv('/workspace/stores.csv')
features = pd.read_csv('/workspace/features.csv')

train_with_stores = pd.merge(train, stores, how='left', on='Store')
test_with_stores = pd.merge(test, stores, how='left', on='Store')
train_with_features = pd.merge(train_with_stores, features, how='left', on=['Store', 'Date'])
test_with_features = pd.merge(test_with_stores, features, how='left', on=['Store', 'Date'])

# Check if 'IsHoliday_x' and 'IsHoliday_y' are identical
print((train_with_features['IsHoliday_x'] == train_with_features['IsHoliday_y']).all())
print((test_with_features['IsHoliday_x'] == test_with_features['IsHoliday_y']).all())

# If they are identical, we can drop 'IsHoliday_y' and rename 'IsHoliday_x' to 'IsHoliday'
if (train_with_features['IsHoliday_x'] == train_with_features['IsHoliday_y']).all():
    train_with_features.drop('IsHoliday_y', axis=1, inplace=True)
    train_with_features.rename(columns={'IsHoliday_x': 'IsHoliday'}, inplace=True)

if (test_with_features['IsHoliday_x'] == test_with_features['IsHoliday_y']).all():
    test_with_features.drop('IsHoliday_y', axis=1, inplace=True)
    test_with_features.rename(columns={'IsHoliday_x': 'IsHoliday'}, inplace=True)

# Handle missing values in MarkDown columns - for simplicity, we'll fill missing values with 0
markdown_columns = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
train_with_features[markdown_columns] = train_with_features[markdown_columns].fillna(0)
test_with_features[markdown_columns] = test_with_features[markdown_columns].fillna(0)

# Encode the 'Type' categorical variable
train_with_features['Type'] = train_with_features['Type'].astype('category').cat.codes
test_with_features['Type'] = test_with_features['Type'].astype('category').cat.codes

# Display the cleaned dataframes
print(train_with_features.head())
print(test_with_features.head())
