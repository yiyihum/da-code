import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from feature_engine.imputation import MeanMedianImputer, CategoricalImputer
from feature_engine.encoding import RareLabelEncoder, OneHotEncoder
import optuna
import xgboost as xgb

train = pd.read_csv("../train.csv")
train.columns = [col.lower() for col in train.columns]

train.dropna(subset=["price"], inplace=True)
train = train[train['price'].apply(lambda x: x.isnumeric())]
train['price'] = train['price'].astype(int)
target_var = 'price'
binary_vars = [col for col in train.columns if train[col].nunique() == 2]
cat_vars = [ col for col in train.columns if col not in binary_vars and train[col].dtype == "object"]
num_vars = [ col for col in train.columns if col not in binary_vars and train[col].dtype in ['int64', 'float64'] and col != target_var]
# Let's approximate the outlier value as 150k
outlier_price = 150000
train = train[train['price'] < outlier_price]

outlier_engine_size = train['engine_size'].quantile(0.999)
train = train[train['engine_size'] < outlier_engine_size]
use_cat_vars = ["brand", "fuel_type", "drivetrain"]
del_cat_vars = list(set(cat_vars) - set(use_cat_vars))
train.drop(del_cat_vars, axis=1, inplace=True)

train, valid = train_test_split(train, test_size=0.15, random_state=0)
X_train = train.drop(target_var, axis=1)
y_train = train[target_var]

X_valid = valid.drop(target_var, axis=1)
y_valid = valid[target_var]

preprocessor_pipe = Pipeline([
    ("num_var_imputer", MeanMedianImputer(imputation_method="median", variables=num_vars+binary_vars)),
    ("cat_var_imputer", CategoricalImputer(imputation_method="frequent", variables=use_cat_vars)),
    ("rare_label_encoder", RareLabelEncoder(
    tol=0.03, n_categories=2, variables=use_cat_vars)),
    ("one_hot_encoder", OneHotEncoder(
    variables=use_cat_vars, ignore_format=True)),
    ("scaling", StandardScaler()),
])

X_train_transformed = preprocessor_pipe.fit_transform(X_train)
X_valid_transformed = preprocessor_pipe.transform(X_valid)

dtrain = xgb.DMatrix(X_train_transformed, label=y_train)
dvalid = xgb.DMatrix(X_valid_transformed, label=y_valid)

def objective(trial):
        
    params = {
        "verbosity": 0, 
        "objective": "reg:squarederror",
        "n_estimators": trial.suggest_int('n_estimators', 50, 500, 50),
        "max_depth": trial.suggest_int("max_depth", 3, 100),
        "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.1, log=True),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.2, 0.6, log=True),
        "subsample": trial.suggest_float("subsample", 0.4, 0.8, log=True),
        "alpha": trial.suggest_float("alpha", 0.01, 10.0, log=True),
        "lambda": trial.suggest_float("lambda", 1e-8, 10.0, log=True),
        "gamma": trial.suggest_float("gamma", 1e-8, 10.0, log=True),
        "min_child_weight": trial.suggest_float("min_child_weight", 10, 1000, log=True),
        "seed": 42
    }

    booster = xgb.train(
    params=params,
    dtrain=dtrain,
    num_boost_round=1000,
    evals=[(dvalid, 'validation')],
    early_stopping_rounds=25
    )

    y_pred = booster.predict(dvalid)
    rmse = mean_squared_error(y_valid, y_pred, squared=False)

    return rmse

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=10)

xgb_best_param = study.best_params
xgb_best_score = study.best_value
xgb_best_param = dict(**xgb_best_param, seed=42)

booster = xgb.train(
    params=xgb_best_param,
    dtrain=dtrain,
    num_boost_round=1000,
    evals=[(dvalid, 'validation')],
    early_stopping_rounds=25
    )

y_pred = booster.predict(dvalid)

test = pd.read_csv("../test.csv")
test.drop(del_cat_vars, axis=1, inplace=True)
X_test = test
y_test = pd.read_csv('./price.csv')[target_var].tolist()


for data in y_test:
    try:
        data = int(data)
    except:
        print(data)
y_test = [int(y_test) for y_test in y_test]
X_test_transformed = preprocessor_pipe.transform(X_test)
dtest = xgb.DMatrix(X_test_transformed)
y_pred = booster.predict(dtest)

result = pd.DataFrame(data=y_pred.tolist(), columns=['price'])

result.to_csv('../price.csv', index=False)