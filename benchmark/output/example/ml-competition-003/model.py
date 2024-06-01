import pandas as pd
from sklearn import svm
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load the training data
train_data = pd.read_csv('train.csv')

# Separate the features and the target variable
X_train = train_data.drop(columns=['Id', 'Class'])
y_train = train_data['Class']

# Define a preprocessor to standardize numeric columns and one-hot encode categorical columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), slice(0, -1)),
        ('cat', OneHotEncoder(), [-1])
    ])

# Fit and transform the training data
X_train = preprocessor.fit_transform(X_train)

# Train a SVM model
model = svm.SVC(probability=True)
model.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('test.csv')

# Separate the features
X_test = test_data.drop(columns=['Id'])

# Transform the test data using the same preprocessor
X_test = preprocessor.transform(X_test)

# Make predictions
y_pred = model.predict_proba(X_test)

# Create a submission dataframe
submission = pd.DataFrame(y_pred, columns=['class_0', 'class_1'])
submission.insert(0, 'Id', test_data['Id'])

# Write the submission dataframe to a csv file
submission.to_csv('submission.csv', index=False)
