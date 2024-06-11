from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import pandas as pd

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Drop the 'CustomerId', 'Surname', and 'id' columns as they are not features
train_df.drop(['CustomerId', 'Surname', 'id'], axis=1, inplace=True)

# Separate features and target variable
X = train_df.drop('Exited', axis=1)
y = train_df['Exited']

# Preprocessing for numerical data
numerical_transformer = StandardScaler()

# Preprocessing for categorical data
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, X.select_dtypes(exclude=['object']).columns),
        ('cat', categorical_transformer, X.select_dtypes(include=['object']).columns)
    ])

# Define the model
model = RandomForestClassifier(n_estimators=100, random_state=0)

# Bundle preprocessing and modeling code in a pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model', model)])

# Split data into train and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
clf.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = clf.predict_proba(X_valid)[:, 1]

# Evaluate the model
score = roc_auc_score(y_valid, preds)
print('AUC score:', score)

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Keep the 'CustomerId' column to use as the submission index
test_ids = test_df['CustomerId']

# Drop the 'CustomerId' and 'Surname' columns as they are not features
test_df.drop(['CustomerId', 'Surname'], axis=1, inplace=True)

# Preprocessing of test data, get predictions
test_preds = clf.predict_proba(test_df)[:, 1]

# Generate submission file
submission = pd.DataFrame({'id': test_ids, 'Exited': test_preds})
submission.to_csv('/workspace/submission.csv', index=False)
