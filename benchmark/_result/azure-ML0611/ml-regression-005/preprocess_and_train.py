import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Convert all 'price' values to strings and remove rows with non-numeric 'price' values
train_data = train_data[train_data['price'].astype(str).str.replace('.', '').str.isdigit()]

# Convert 'price' to float
train_data['price'] = train_data['price'].astype(float)

# Separate the target variable (price) from the predictors
y = train_data['price']
X = train_data.drop(['price'], axis=1)

# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='mean')

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, X.select_dtypes(exclude=['object']).columns),
        ('cat', categorical_transformer, X.select_dtypes(include=['object']).columns)
    ])

# Define the model as Linear Regression
model = LinearRegression()

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
score = mean_squared_error(y_valid, preds, squared=False)
print(f'Mean Squared Error: {score}')

# Save the model to a file
pd.to_pickle(clf, '/workspace/car_price_model.pkl')

print("Model training complete and model saved.")
