import pandas as pd

# Load the datasets
train_df = pd.read_csv('/workspace/train.csv')
test_df = pd.read_csv('/workspace/test.csv')
features_df = pd.read_csv('/workspace/features.csv', na_values=['NA'])
stores_df = pd.read_csv('/workspace/stores.csv')

# Merge the features and stores with the train and test datasets
train_merged = pd.merge(train_df, features_df, on=['Store', 'Date', 'IsHoliday'], how='left')
train_merged = pd.merge(train_merged, stores_df, on='Store', how='left')

test_merged = pd.merge(test_df, features_df, on=['Store', 'Date', 'IsHoliday'], how='left')
test_merged = pd.merge(test_merged, stores_df, on='Store', how='left')

# Fill missing values for MarkDowns with 0 (assuming no markdown)
markdown_columns = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
train_merged[markdown_columns] = train_merged[markdown_columns].fillna(0)
test_merged[markdown_columns] = test_merged[markdown_columns].fillna(0)

# Fill missing values for CPI and Unemployment with their median values
cpi_median = train_merged['CPI'].median()
unemployment_median = train_merged['Unemployment'].median()
train_merged['CPI'] = train_merged['CPI'].fillna(cpi_median)
train_merged['Unemployment'] = train_merged['Unemployment'].fillna(unemployment_median)
test_merged['CPI'] = test_merged['CPI'].fillna(cpi_median)
test_merged['Unemployment'] = test_merged['Unemployment'].fillna(unemployment_median)

# Encode categorical variables (Type and IsHoliday)
train_merged['Type'] = train_merged['Type'].astype('category').cat.codes
test_merged['Type'] = test_merged['Type'].astype('category').cat.codes
train_merged['IsHoliday'] = train_merged['IsHoliday'].astype(int)
test_merged['IsHoliday'] = test_merged['IsHoliday'].astype(int)

# Save the prepared datasets to CSV files
train_merged.to_csv('/workspace/train_prepared.csv', index=False)
test_merged.to_csv('/workspace/test_prepared.csv', index=False)

# Output the first few rows of the prepared train dataset
print(train_merged.head())
