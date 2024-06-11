import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Assuming the 'outcome' column is missing, we will drop the 'id.1' column as it is a duplicate of 'id'
train_df = train_df.drop(columns=['id.1'])

# Preprocessing: Fill missing values and encode categorical variables
train_df = train_df.ffill().bfill()
label_encoders = {}
for column in train_df.select_dtypes(include=['object']).columns:
    label_encoders[column] = LabelEncoder()
    train_df[column] = label_encoders[column].fit_transform(train_df[column])

# Split the data into features and target; here we assume the target is the last column
X = train_df.iloc[:, :-1]
y = train_df.iloc[:, -1]

# Drop the 'id' column as it is not a feature
X = X.drop(columns=['id'])

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_clf.fit(X_train, y_train)

# Validate the model
y_pred_val = rf_clf.predict(X_val)
val_f1_score = f1_score(y_val, y_pred_val, average='micro')
print(f"Validation F1 Score: {val_f1_score}")

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Preprocessing: Fill missing values and encode categorical variables
test_df = test_df.ffill().bfill()
for column in test_df.select_dtypes(include=['object']).columns:
    if column in label_encoders:
        test_df[column] = label_encoders[column].transform(test_df[column])
    else:
        test_df[column] = LabelEncoder().fit_transform(test_df[column])

# Predict on the test data
test_predictions = rf_clf.predict(test_df.drop(columns=['id']))

# Create the submission dataframe
submission_df = pd.DataFrame({'id': test_df['id'], 'outcome': test_predictions})

# Save the submission file
submission_df.to_csv('/workspace/submission.csv', index=False)
