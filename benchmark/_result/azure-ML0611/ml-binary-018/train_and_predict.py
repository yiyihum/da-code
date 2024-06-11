import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset for training
data = pd.read_csv('healthcare-dataset-stroke-data.csv')

# Separate features and target variable
X = data.drop(columns=['id', 'stroke'])
y = data['stroke']

# Preprocessing for numerical data
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']),
        ('cat', categorical_transformer, ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status'])
    ])

# Define the model
model = RandomForestClassifier(n_estimators=100, random_state=0)

# Bundle preprocessing and modeling code in a pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model', model)])

# Split the dataset into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
clf.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = clf.predict(X_valid)

# Evaluate the model
score = accuracy_score(y_valid, preds)
print(f'Accuracy: {score:.4f}')

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocessing of test data, fit model
test_preds = clf.predict(test_data.drop(columns=['id']))

# Save the predictions to a CSV file
output = pd.DataFrame({'stroke': test_preds})
output.to_csv('stroke.csv', index=False)
