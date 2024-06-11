import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Re-merge the datasets since the previous merged dataframes are not saved as CSV files
train = pd.read_csv('/workspace/train.csv')
test = pd.read_csv('/workspace/test.csv')
stores = pd.read_csv('/workspace/stores.csv')
features = pd.read_csv('/workspace/features.csv')

train_with_stores = pd.merge(train, stores, how='left', on='Store')
test_with_stores = pd.merge(test, stores, how='left', on='Store')
train_with_features = pd.merge(train_with_stores, features, how='left', on=['Store', 'Date'])
test_with_features = pd.merge(test_with_stores, features, how='left', on=['Store', 'Date'])

# Clean the data as before
train_with_features['IsHoliday'] = train_with_features['IsHoliday_x']
train_with_features.drop(['IsHoliday_x', 'IsHoliday_y'], axis=1, inplace=True)
test_with_features['IsHoliday'] = test_with_features['IsHoliday_x']
test_with_features.drop(['IsHoliday_x', 'IsHoliday_y'], axis=1, inplace=True)
markdown_columns = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
train_with_features[markdown_columns] = train_with_features[markdown_columns].fillna(0)
test_with_features[markdown_columns] = test_with_features[markdown_columns].fillna(0)
train_with_features['Type'] = train_with_features['Type'].astype('category').cat.codes
test_with_features['Type'] = test_with_features['Type'].astype('category').cat.codes

# Convert 'Date' to datetime and extract year, month, and week
train_with_features['Date'] = pd.to_datetime(train_with_features['Date'])
test_with_features['Date'] = pd.to_datetime(test_with_features['Date'])
train_with_features['Year'] = train_with_features['Date'].dt.year
train_with_features['Month'] = train_with_features['Date'].dt.month
train_with_features['Week'] = train_with_features['Date'].dt.isocalendar().week
test_with_features['Year'] = test_with_features['Date'].dt.year
test_with_features['Month'] = test_with_features['Date'].dt.month
test_with_features['Week'] = test_with_features['Date'].dt.isocalendar().week

# Drop the 'Date' column as we have extracted the year, month, and week
train_with_features.drop('Date', axis=1, inplace=True)
test_with_features.drop('Date', axis=1, inplace=True)

# Prepare the data for training
X = train_with_features.drop('Weekly_Sales', axis=1)
y = train_with_features['Weekly_Sales']

# Split the data into training and validation sets
X_train, X_validation, y_train, y_validation = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Regressor with fewer estimators to reduce training time
rf = RandomForestRegressor(n_estimators=10, random_state=42)
rf.fit(X_train, y_train)

# Validate the model
validation_predictions = rf.predict(X_validation)

# Calculate the mean absolute error as a simple validation metric
mae = sum(abs(y_validation - validation_predictions)) / len(validation_predictions)
print(f'Mean Absolute Error: {mae}')
