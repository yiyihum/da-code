import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

# Load the dataset
data = pd.read_csv('weatherAUS.csv')

# Preprocess the data
# Drop rows with missing target, separate target from predictors
data.dropna(axis=0, subset=['RainTomorrow'], inplace=True)
y = data.RainTomorrow
X = data.drop(['RainTomorrow'], axis=1)

# To keep things simple, we'll use only numerical predictors
X = X.select_dtypes(exclude=['object'])

# Break off validation set from training data
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Imputation
my_imputer = SimpleImputer()
imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))
imputed_X_valid = pd.DataFrame(my_imputer.transform(X_valid))

# Imputation removed column names; put them back
imputed_X_train.columns = X_train.columns
imputed_X_valid.columns = X_valid.columns

# Define the model
model = RandomForestClassifier(n_estimators=100, random_state=0)

# Fit the model
model.fit(imputed_X_train, y_train)

# Get validation predictions and print accuracy
preds = model.predict(imputed_X_valid)
print('Accuracy:', accuracy_score(y_valid, preds))

# Save the model
import joblib
joblib.dump(model, 'rain_model.joblib')
