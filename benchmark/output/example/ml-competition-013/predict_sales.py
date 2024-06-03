import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load the data
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Preprocess the data
train_data.dropna(axis=0, subset=['num_sold'], inplace=True)
y = train_data.num_sold
X = train_data.drop(['num_sold'], axis=1).select_dtypes(exclude=['object'])
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=0)

# Define and fit the model
model = RandomForestRegressor(n_estimators=100, random_state=0)
model.fit(train_X, train_y)

# Make predictions and calculate the error
val_predictions = model.predict(val_X)
print("Mean Absolute Error: ", mean_absolute_error(val_y, val_predictions))

# Make predictions on the test data
final_X_test = test_data.select_dtypes(exclude=['object'])
final_predictions = model.predict(final_X_test)

# Save the predictions to a CSV file
output = pd.DataFrame({'id': test_data.id, 'num_sold': final_predictions})
output.to_csv('submission.csv', index=False)
