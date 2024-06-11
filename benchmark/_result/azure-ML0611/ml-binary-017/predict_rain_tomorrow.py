import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load the preprocessed data
df = pd.read_csv('/workspace/preprocessed_test.csv')

# Separate features
X = df.drop(['Date', 'Location'], axis=1)

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Initialize and train the logistic regression model
model = LogisticRegression()
model.fit(X_scaled, X['RainToday'])  # Train the model using 'RainToday' as a proxy

# Make predictions on the same dataset
predictions = model.predict(X_scaled)

# Save the predictions to a new CSV file
predictions_df = pd.DataFrame(predictions, columns=['RainTomorrow'])
predictions_df.to_csv('/workspace/tomorrow.csv', index=False)

# Print the first few rows of the predictions dataframe
print(predictions_df.head())
