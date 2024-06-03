import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import StackingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor

original_train = pd.read_csv('../abalone.data', header=None)
train = pd.read_csv('../train.csv')
test = pd.read_csv('../test.csv')
sample_submission = pd.read_csv('../sample_submission.csv')

original_train.columns = train.columns[1:]
submission_id = test.id

train.drop(columns='id', axis=1, inplace=True)
test.drop(columns='id', axis=1, inplace=True)
train = pd.concat(objs=[train, original_train])

train_duplicates_number = train[train.duplicated()]
test_duplicates_number = test[test.duplicated()]

train = train.drop_duplicates()
# Check whether all duplicates were removed
train_duplicates = train[train.duplicated()]

X = pd.get_dummies(train, drop_first=True, dtype=int)
test = pd.get_dummies(test, drop_first=True, dtype=int)

# Split the train data into X and y
X = X.drop(['Rings'], axis=1)
y = train.Rings

best_forest = RandomForestRegressor(
    random_state=27,
)
    
best_forest.fit(X, y)
importance = best_forest.feature_importances_
feature_importance = pd.DataFrame(data=importance, index=X.columns, columns=['importance']) \
    .sort_values(ascending=True, by='importance')

numeric_columns_train = X.select_dtypes(include=np.number)
corr_train = numeric_columns_train.corr(method='pearson')
mask_train = np.triu(np.ones_like(corr_train))
X = X.drop(['Diameter', 'Whole weight.2', 'Whole weight'], axis=1)
test = test.drop(['Diameter', 'Whole weight.2', 'Whole weight'], axis=1)
numeric_columns_train = X.select_dtypes(include=np.number)
corr_train = numeric_columns_train.corr(method='pearson')
mask_train = np.triu(np.ones_like(corr_train))
# Split data into train and val
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=27)

base_models = [
    ('XGBoost', XGBRegressor(
        random_state=27
    )),
    ('LightGBM', LGBMRegressor(
        random_state=27
    )),
    ('Catboost', CatBoostRegressor(
    random_state=27
    )),
    ('RandomForest', RandomForestRegressor(
        random_state=27
    ))
]

meta_model = CatBoostRegressor(
    iterations=101,
    learning_rate=0.0010172906333606835,
    colsample_bylevel=0.4796381789116622,
    min_data_in_leaf=42,
    depth=13,
    l2_leaf_reg=2.895211427077531e-08,
    random_state=27,
)
stacking_model = StackingRegressor(estimators=base_models, final_estimator=meta_model)

stacking_model.fit(X, y)

y_pred_test = stacking_model.predict(test)

submission = pd.DataFrame({
    'id': sample_submission.id,
    'Rings': y_pred_test
})

submission.to_csv('../submission.csv', index=False)

