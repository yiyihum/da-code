import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target variable
X_train = train_data.drop(columns=['Exited', 'CustomerId', 'Surname'])
y_train = train_data['Exited']

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

# Split the training data for validation
X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, train_size=0.8, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
clf.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = clf.predict_proba(X_valid)[:, 1]

# Calculate ROC AUC score
roc_auc = roc_auc_score(y_valid, preds)
print(f'ROC AUC score: {roc_auc}')

# Save the model to a file
import joblib
joblib.dump(clf, '/workspace/churn_model.joblib')
