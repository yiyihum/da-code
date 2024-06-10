import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the datasets
train_df = pd.read_csv('/workspace/Output.csv', delimiter=';')
test_df = pd.read_csv('/workspace/test.csv')

# Replace commas with periods in the 'Star rating', 'Set Price', and 'Number of reviews' columns and convert to float
train_df['Star rating'] = train_df['Star rating'].str.replace(',', '.').astype(float)
train_df['Set Price'] = train_df['Set Price'].str.replace(',', '.').astype(float)
train_df['Number of reviews'] = train_df['Number of reviews'].str.replace(',', '.').astype(float)
test_df['Set Price'] = test_df['Set Price'].str.replace(',', '.').astype(float)
test_df['Number of reviews'] = test_df['Number of reviews'].str.replace(',', '.').astype(float)

# Sample a very small subset of the training data to speed up the training process
train_sample = train_df.sample(frac=0.001, random_state=42)

# Select only numerical features for the model
numerical_columns = ['year', 'Set Price', 'Number of reviews']
X_train = train_sample[numerical_columns]
y_train = train_sample['Star rating']
X_test = test_df[numerical_columns]

# Train a simpler model without scaling
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the star ratings
predictions = model.predict(X_test)

# Save the predictions to a CSV file
result_df = test_df.copy()
result_df['Star rating'] = predictions
result_df[['Star rating']].to_csv('/workspace/result.csv', index=False)
