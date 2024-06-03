# Data manipulation and analysis libraries
import pandas as pd
import numpy as np

# Preprocessing and model evaluation libraries
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import (
    train_test_split
)

# Sampling libraries
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

# Pipeline and transformation libraries
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

# Model building libraries
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier
)


train_data = pd.read_csv('../Train.csv')
test_data = pd.read_csv('../Test.csv')

# View top 5 rows of the data
train_data.head()
# View top 5 rows of the data
test_data.head()
# Check the dimensions of the data
train_data.shape
test_data.shape
# Double check for null values per column
train_data.isnull().sum()
test_data.isnull().sum()

train_df = train_data.copy()
test_df = test_data.copy()
X = train_df.drop(["Target"], axis=1)
y = train_df["Target"]

X_train = X
y_train = y
X_test = test_df
# Create an instance of the imputer
imputer = SimpleImputer(strategy="median")
# Fit on the training data and transform it
X_train = pd.DataFrame(imputer.fit_transform(X_train), columns=X_train.columns)
# Transform the test data based on the fit from the training data
X_test = pd.DataFrame(imputer.transform(X_test), columns=X_test.columns)

# Create a scaler instance
scaler = StandardScaler()
# Fit on the training data and transform it
X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
# Transform the validation and test data
X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

# defining a function to compute different metrics to check performance of a classification model built using sklearn

sm = SMOTE(sampling_strategy=1, k_neighbors=5, random_state=1)

pipe = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("AdaBoost", AdaBoostClassifier
         (
               n_estimators=128,
               algorithm='SAMME',
               learning_rate=1e-3,
               estimator=DecisionTreeClassifier(max_depth=10, random_state=42),
            ),
        ),
    ]
)

pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

result = pd.DataFrame(data=y_pred.tolist(), columns=['Target'])
result.to_csv('../target.csv', index=False)

