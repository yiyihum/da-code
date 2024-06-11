import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('Output.csv', delimiter=';')

# Preprocess the data: Encode categorical variables, handle missing values, etc.
# For simplicity, I will only use numeric columns and ignore URLs and names.
train_data['Set Price'] = train_data['Set Price'].str.replace(',', '.').astype(float)
train_data['Number of reviews'] = train_data['Number of reviews'].str.replace(',', '.').astype(float)
train_data['Star rating'] = train_data['Star rating'].str.replace(',', '.').astype(float)

# Selecting features and target variable
features = ['year', 'Set Price', 'Number of reviews']
target = 'Star rating'

# Encoding categorical variables (if any)
# For this example, I'm skipping this step as we're only using numeric features

# Splitting the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(train_data[features], train_data[target], test_size=0.2, random_state=42)

# Initialize the model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f'Mean Squared Error: {mse}')

# Load the test data
test_data = pd.read_csv('test.csv')
test_data['Set Price'] = test_data['Set Price'].str.replace(',', '.').astype(float)
test_data['Number of reviews'] = test_data['Number of reviews'].str.replace(',', '.').astype(float)

# Predict the star rating for the test data
test_data['Star rating'] = model.predict(test_data[features])

# Save the predictions to a CSV file
test_data[['Star rating']].to_csv('result.csv', index=False)
