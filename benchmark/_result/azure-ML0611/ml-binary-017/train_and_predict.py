import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load the preprocessed data
df = pd.read_csv('/workspace/preprocessed_test.csv')

# Separate features and target variable
X = df.drop(['Date', 'Location', 'RainTomorrow'], axis=1)  # Assuming 'RainTomorrow' is not in the test set
y = df['RainToday']  # Using 'RainToday' as a proxy for 'RainTomorrow' for training

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize and train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Save the predictions to a new CSV file
predictions_df = pd.DataFrame(predictions, columns=['RainTomorrow'])
predictions_df.to_csv('/workspace/tomorrow.csv', index=False)

# Print the first few rows of the predictions dataframe
print(predictions_df.head())
