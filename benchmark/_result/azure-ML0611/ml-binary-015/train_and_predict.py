import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load the preprocessed data
train_data = pd.read_csv('/workspace/preprocessed_train.csv')
test_data = pd.read_csv('/workspace/preprocessed_test.csv')

# Separate features and target variable
X_train = train_data.drop('CLASS', axis=1)
y_train = train_data['CLASS']

# Initialize the Logistic Regression model
model = LogisticRegression(max_iter=1000)

# Fit the model on the training data
model.fit(X_train, y_train)

# Predict the 'CLASS' for the test data
predictions = model.predict(test_data)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(predictions, columns=['CLASS'])
predictions_df.to_csv('/workspace/class.csv', index=False)

# Output the path to the saved predictions file
print('/workspace/class.csv')
