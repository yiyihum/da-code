import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the train.csv file into a DataFrame
df = pd.read_csv('train.csv')

# Encode the 'Sex' column
le = LabelEncoder()
df['Sex'] = le.fit_transform(df['Sex'])

# Split the DataFrame into features and target variable
X = df.drop(columns=['id', 'Rings'])
y = df['Rings']

# Train a Linear Regression model
lr = LinearRegression()
lr.fit(X, y)

# Load the test.csv file into a DataFrame
test_df = pd.read_csv('test.csv')

# Encode the 'Sex' column in the test DataFrame
test_df['Sex'] = le.transform(test_df['Sex'])

# Extract the id column from the test DataFrame
test_ids = test_df['id']

# Drop the id column from the test DataFrame
test_df = test_df.drop(columns=['id'])

# Make predictions on the test DataFrame
test_preds = lr.predict(test_df)

# Create a submission DataFrame
submission_df = pd.DataFrame({'id': test_ids, 'Rings': test_preds})

# Write the submission DataFrame to a CSV file
submission_df.to_csv('submission.csv', index=False)
