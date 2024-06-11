import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Load the training data
train_data = pd.read_csv('/workspace/Cleaned_airbnb_barcelona.csv')

# Preprocess the 'price' column to remove the dollar sign and convert to float
train_data['price'] = train_data['price'].replace('[\$,]', '', regex=True).astype(float)

# Separate target from predictors
y = train_data['price']
X = train_data.drop(['price', 'id.1'], axis=1)  # Drop 'id.1' and 'price' columns

# Select categorical columns with relatively low cardinality (convenient but arbitrary)
categorical_cols = [cname for cname in X.columns if
                    X[cname].nunique() < 10 and 
                    X[cname].dtype == "object"]

# Select numerical columns
numerical_cols = [cname for cname in X.columns if 
                  X[cname].dtype in ['int64', 'float64']]

# Keep selected columns only
my_cols = categorical_cols + numerical_cols
X = X[my_cols].copy()
X_test = test_data[my_cols].copy()

# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='constant')

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Define the model
model = RandomForestRegressor(n_estimators=100, random_state=0)

# Bundle preprocessing and modeling code in a pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model', model)
                     ])

# Preprocessing of training data, fit model 
clf.fit(X, y)

# Preprocessing of test data, get predictions
preds = clf.predict(X_test)

# Save the predictions to a CSV file
output = pd.DataFrame({'id': test_data.id,
                       'price': preds})
output.to_csv('/workspace/price.csv', index=False)
