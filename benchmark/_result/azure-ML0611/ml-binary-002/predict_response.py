import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X = train_data.drop(columns=['id', 'Response'])
y = train_data['Response']

# Preprocessing for numerical data
numerical_cols = [cname for cname in X.columns if X[cname].dtype in ['int64', 'float64']]
numerical_transformer = StandardScaler()

# Preprocessing for categorical data
categorical_cols = [cname for cname in X.columns if X[cname].dtype == "object"]
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
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
preds = clf.predict(X_valid)

# Evaluate the model
score = accuracy_score(y_valid, preds)
print(f'Accuracy: {score:.4f}')

# Save the model (optional, in case of further tuning or analysis)
# joblib.dump(clf, 'model.joblib')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')
X_test = test_data.drop(columns=['id'])

# Preprocessing of test data, get predictions
test_preds = clf.predict(X_test)

# Save the predictions in the submission format
submission = pd.DataFrame({'id': test_data['id'], 'Response': test_preds})
submission.to_csv('/workspace/submission.csv', index=False)
