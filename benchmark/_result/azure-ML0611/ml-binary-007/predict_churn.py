import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the datasets
train_df = pd.read_csv('customer_churn_dataset-training-master.csv')
test_df = pd.read_csv('customer_churn_dataset-testing-master.csv')

# Separate features and target from training data
X_train = train_df.drop(['CustomerID', 'Churn'], axis=1)
y_train = train_df['Churn']

# Preprocessing for numerical data
numerical_cols = [cname for cname in X_train.columns if X_train[cname].dtype in ['int64', 'float64']]
numerical_transformer = StandardScaler()

# Preprocessing for categorical data
categorical_cols = [cname for cname in X_train.columns if X_train[cname].dtype == "object"]
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

# Preprocessing of training data, fit model
clf.fit(X_train, y_train)

# Preprocess test data
X_test = test_df.drop(['CustomerID'], axis=1)

# Predict on test data
test_preds = clf.predict(X_test)

# Save the predictions to a CSV file
output = pd.DataFrame({'CustomerID': test_df.CustomerID, 'result': test_preds})
output.to_csv('result.csv', index=False)
