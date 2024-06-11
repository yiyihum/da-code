import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load the training and test data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Preprocessing
# Convert 'date' to datetime and extract relevant features
train_data['date'] = pd.to_datetime(train_data['date'])
test_data['date'] = pd.to_datetime(test_data['date'])

# Extract year, month, day from the date
for df in [train_data, test_data]:
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

# Drop the original 'date' column
train_data.drop('date', axis=1, inplace=True)
test_data.drop('date', axis=1, inplace=True)

# Convert categorical variables to dummy variables
train_data = pd.get_dummies(train_data, columns=['country', 'store', 'product'])
test_data = pd.get_dummies(test_data, columns=['country', 'store', 'product'])

# Ensure the columns match in train and test sets
test_data = test_data.reindex(columns=train_data.columns, fill_value=0)
test_data.drop(['num_sold'], axis=1, inplace=True)

# Save the 'id' column for the submission file
test_ids = test_data['id']
test_data.drop(['id'], axis=1, inplace=True)

# Split the training data into features and target
X = train_data.drop(['id', 'num_sold'], axis=1)
y = train_data['num_sold']

# Split data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=0)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_valid)
mae = mean_absolute_error(y_valid, y_pred)
print(f'Mean Absolute Error: {mae}')

# Predict on the test data
test_preds = model.predict(test_data)

# Prepare the submission file
submission = pd.DataFrame({'id': test_ids, 'num_sold': test_preds})
submission.to_csv('/workspace/submission.csv', index=False)
