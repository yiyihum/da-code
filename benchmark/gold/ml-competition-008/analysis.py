import numpy as np 
import pandas as pd 
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import (
    SGDRegressor, 
    BayesianRidge,
)
import warnings 
warnings.filterwarnings('ignore') 

flood_dataset = pd.read_csv("../train.csv")      
flood_dataset_test_df = pd.read_csv("../test.csv")
flood_dataset.drop(columns=['id'], inplace=True)
flood_dataset_train = flood_dataset.drop(['FloodProbability'],axis=1)

scaler = StandardScaler()
scaler.fit(flood_dataset_train)
flood_dataset_train = scaler.transform(flood_dataset_train)
dependent_var = flood_dataset['FloodProbability']
Encode_Data = preprocessing.LabelEncoder()
dependent_var_transformed = Encode_Data.fit_transform(dependent_var)
flood_dataset_train_partially = flood_dataset_train[:1500].copy()
dependent_var_transformed_partially = dependent_var_transformed[:1500].copy()

model_LR=LogisticRegression(solver="liblinear")
model_LR.fit(flood_dataset_train_partially, dependent_var_transformed_partially)
feature_importance = model_LR.coef_[0]

X_train = flood_dataset_train
y_train = dependent_var_transformed
est = [('model_SGD', SGDRegressor()), ('model_BF',BayesianRidge()),('model_LR',LinearRegression())] 
stacked = StackingRegressor(estimators=est,final_estimator=RandomForestRegressor(n_estimators=50,max_depth=5))
stacked.fit(X_train,y_train)

id_no = flood_dataset_test_df['id']
flood_dataset_test_df.drop('id',axis=1,inplace=True)
scaler = StandardScaler()
scaler.fit(flood_dataset_test_df)
flood_dataset_test_df = scaler.transform(flood_dataset_test_df)
testdata_y_pred = stacked.predict(flood_dataset_test_df)
final_predictions = testdata_y_pred.flatten() 
result = pd.DataFrame({'id':id_no,'FloodProbability':testdata_y_pred/100})
result.to_csv('./submission.csv', index=False)