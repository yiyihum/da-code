import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Re-merge and clean the datasets as before
train = pd.read_csv('/workspace/train.csv')
test = pd.read_csv('/workspace/test.csv')
stores = pd.read_csv('/workspace/stores.csv')
features = pd.read_csv('/workspace/features.csv')

train_with_stores = pd.merge(train, stores, how='left', on='Store')
test_with_stores = pd.merge(test, stores, how='left', on='Store')
train_with_features = pd.merge(train_with_stores, features, how='left', on=['Store', 'Date'])
test_with_features = pd.merge(test_with_stores, features, how='left', on=['Store', 'Date'])

train_with_features['IsHoliday'] = train_with_features['IsHoliday_x']
train_with_features.drop(['IsHoliday_x', 'IsHoliday_y'], axis=1, inplace=True)
test_with_features['IsHoliday'] = test_with_features['IsHoliday_x']
test_with_features.drop(['IsHoliday_x', 'IsHoliday_y'], axis=1, inplace=True)
markdown_columns = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
train_with_features[markdown_columns] = train_with_features[markdown_columns].fillna(0)
test_with_features[markdown_columns] = test_with_features[markdown_columns].fillna(0)
train_with_features['Type'] = train_with_features['Type'].astype('category').cat.codes
test_with_features['Type'] = test_with_features['Type'].astype('category').cat.codes

train_with_features['Date'] = pd.to_datetime(train_with_features['Date'])
test_with_features['Date'] = pd.to_datetime(test_with_features['Date'])
train_with_features['Year'] = train_with_features['Date'].dt.year
train_with_features['Month'] = train_with_features['Date'].dt.month
train_with_features['Week'] = train_with_features['Date'].dt.isocalendar().week
test_with_features['Year'] = test_with_features['Date'].dt.year
test_with_features['Month'] = test_with_features['Date'].dt.month
test_with_features['Week'] = test_with_features['Date'].dt.isocalendar().week

train_with_features.drop('Date', axis=1, inplace=True)
test_with_features.drop('Date', axis=1, inplace=True)

X_train = train_with_features.drop('Weekly_Sales', axis=1)
y_train = train_with_features['Weekly_Sales']
X_test = test_with_features

# Train the Random Forest Regressor with the same parameters as before
rf = RandomForestRegressor(n_estimators=10, random_state=42)
rf.fit(X_train, y_train)

# Make predictions on the test set
test_predictions = rf.predict(X_test)

# Prepare the submission file
submission = pd.DataFrame({'Weekly_Sales': test_predictions})
submission.to_csv('/workspace/submission.csv', index=False)
print(submission.head())
