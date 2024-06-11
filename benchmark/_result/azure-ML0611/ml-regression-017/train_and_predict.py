import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Function to clean numerical columns
def clean_numerical_columns(df, cols):
    for col in cols:
        df[col] = df[col].astype(str).str.replace(',', '').astype(float)
    return df

# Load the training data
train_data = pd.read_csv('games-release-ALL.csv')

# Preprocess the data
train_data['rating'] = train_data['rating'].str.rstrip('%').astype('float') / 100.0  # Convert percentage to float
train_data = clean_numerical_columns(train_data, ['peak_players', 'positive_reviews', 'negative_reviews', 'total_reviews'])
train_data.fillna(0, inplace=True)  # Fill missing values with 0

# Feature engineering
numerical_cols = ['peak_players', 'positive_reviews', 'negative_reviews', 'total_reviews']
X = train_data[numerical_cols]
y = train_data['rating']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f'Mean Squared Error: {mse}')

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess the test data
test_data = clean_numerical_columns(test_data, ['peak_players', 'positive_reviews', 'negative_reviews', 'total_reviews'])
test_data.fillna(0, inplace=True)  # Fill missing values with 0

# Predict using the model
X_test = test_data[numerical_cols]
test_data['rating'] = model.predict(X_test)

# Save the predictions to a CSV file
test_data[['rating']].to_csv('rating.csv', index=False)
