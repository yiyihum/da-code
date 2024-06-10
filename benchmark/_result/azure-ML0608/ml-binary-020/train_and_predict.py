import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the data
cvd_data = pd.read_csv('/workspace/CVD_cleaned.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Separate features and target
X = cvd_data.drop('Heart_Disease', axis=1)
y = cvd_data['Heart_Disease'].apply(lambda x: 1 if x == 'Yes' else 0)

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

# Split the dataset into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
clf.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = clf.predict(X_valid)

# Evaluate the model
score = accuracy_score(y_valid, preds)
print(f'Accuracy: {score}')

# Preprocess test data and get predictions
test_preds = clf.predict(test_data)

# Save the predictions to a CSV file
output = pd.DataFrame({'Heart_Disease': test_preds})
output['Heart_Disease'] = output['Heart_Disease'].apply(lambda x: 'Yes' if x == 1 else 'No')
output.to_csv('/workspace/disease.csv', index=False)
