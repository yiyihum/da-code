import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer

# Load the data
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Prepare the training data
X_train = train_data.drop(['ID_LAT_LON_YEAR_WEEK', 'emission'], axis=1)
y_train = train_data['emission']

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test data
X_test = test_data.drop('ID_LAT_LON_YEAR_WEEK', axis=1)
X_test = imputer.transform(X_test)
predictions = model.predict(X_test)

# Prepare the submission data
submission = pd.DataFrame({
    'ID_LAT_LON_YEAR_WEEK': test_data['ID_LAT_LON_YEAR_WEEK'],
    'emission': predictions
})

# Write the submission data to a CSV file
submission.to_csv('submission.csv', index=False)
