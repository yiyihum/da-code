import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load the training and test data
train_df = pd.read_csv('/workspace/train.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Split the training data into features and target
X_train = train_df.drop(['id', 'yield'], axis=1)
y_train = train_df['yield']

# Train a Random Forest Regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Predict on the test data
X_test = test_df.drop(['id'], axis=1)
test_df['yield'] = rf.predict(X_test)

# Prepare the submission file
submission_df = test_df[['id', 'yield']]
submission_df.to_csv('/workspace/submission.csv', index=False)

print("Training completed and submission file is ready.")
