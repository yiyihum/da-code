import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# Load the training data
train_data = pd.read_csv('/workspace/Train.csv')

# Select a subset of features for simplicity
features = ['age', 'education', 'employment_stat', 'wage_per_hour']
X = train_data[features]
y = train_data['income_above_limit'].apply(lambda x: 1 if x == 'Above limit' else 0)

# Preprocessing steps
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Preprocess the numerical features
X = numerical_transformer.fit_transform(X)

# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Create the model
model = RandomForestClassifier(n_estimators=100, random_state=0)

# Fit the model
model.fit(X_train, y_train)

# Get predictions
preds = model.predict(X_valid)

# Evaluate the model
score = model.score(X_valid, y_valid)
print('Validation accuracy:', score)
