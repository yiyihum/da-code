import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the train.csv file into a pandas dataframe
train_df = pd.read_csv('train.csv')

# Separate the features and the target variable
X = train_df.drop(['id', 'FloodProbability'], axis=1)
y = train_df['FloodProbability']

# Split the data into training set and validation set
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the probabilities on the validation set
y_val_pred = model.predict(X_val)

# Calculate the mean squared error
mse = mean_squared_error(y_val, y_val_pred)

# Print the mean squared error
print('Mean squared error:', mse)
