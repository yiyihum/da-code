import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Load the dataset
data = pd.read_csv('/workspace/test.csv')

# Select features and target variable
features = data.drop(columns=['profile_id'])
target = data['stator_yoke']  # Assuming stator_yoke temperature as a proxy for rotor temperature

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the rotor temperature on the test set
predictions = model.predict(X_test)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(predictions, columns=['pm'])
predictions_df.to_csv('/workspace/pm.csv', index=False)
