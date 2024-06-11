import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the dataset
df = pd.read_csv('diabetes_prediction_dataset.csv')

# Preprocessing
# Convert categorical features to lowercase to ensure consistency
df['gender'] = df['gender'].str.lower()
df['smoking_history'] = df['smoking_history'].str.lower()

# Encoding categorical features
le_gender = LabelEncoder()
le_smoking_history = LabelEncoder()
df['gender'] = le_gender.fit_transform(df['gender'])
df['smoking_history'] = le_smoking_history.fit_transform(df['smoking_history'])

# Handling missing values
df.fillna(df.mean(), inplace=True)

# Splitting the dataset into features and target variable
X = df.drop(columns=['diabetes'])
y = df['diabetes']

# Splitting the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)

# Model training
model = LogisticRegression()
model.fit(X_train, y_train)

# Validation
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f"Validation Accuracy: {accuracy}")

# Load test data
test_df = pd.read_csv('test.csv')

# Preprocessing test data
test_df['gender'] = test_df['gender'].str.lower()
test_df['smoking_history'] = test_df['smoking_history'].str.lower()
test_df['gender'] = le_gender.transform(test_df['gender'])
test_df['smoking_history'] = le_smoking_history.transform(test_df['smoking_history'])
test_df.fillna(test_df.mean(), inplace=True)

# Ensure the order of columns matches the training data
test_df = test_df[X.columns]

# Scaling test data
test_df = scaler.transform(test_df)

# Predicting diabetes for the test data
predictions = model.predict(test_df)

# Save predictions to a CSV file
output_df = pd.DataFrame(predictions, columns=['diabetes'])
output_df.to_csv('diabetes.csv', index=False)
