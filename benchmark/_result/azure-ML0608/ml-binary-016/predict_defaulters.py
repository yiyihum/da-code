import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('UCI_Credit_Card.csv')

# Preprocess the training data
# Assuming no missing values and all data is numerical and relevant
features = train_data.columns.drop(['ID', 'default.payment.next.month'])
X_train = train_data[features]
y_train = train_data['default.payment.next.month']

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train the logistic regression model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess the test data in the same way as the training data
X_test = test_data[features]
X_test_scaled = scaler.transform(X_test)

# Predict the default status for the test data
test_data['IsDefaulter'] = model.predict(X_test_scaled)

# Save the predictions to a new file
test_data[['ID', 'IsDefaulter']].to_csv('defaulter.csv', index=False)
