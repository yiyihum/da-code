import pandas as pd
import numpy as np
import warnings
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import ExtraTreesRegressor
warnings.filterwarnings('ignore')

df=pd.read_csv('../Clean_Dataset.csv')
test = pd.read_csv('../test.csv')
df=df.drop('Unnamed: 0',axis=1)
test=test.drop('Unnamed: 0',axis=1)

le=LabelEncoder()
for col in df.columns:
    if df[col].dtype=='object':
        df[col]=le.fit_transform(df[col])
    if col in test.columns:
        if test[col].dtype=='object':
            test[col]=le.fit_transform(test[col])

x_train=df.drop(['price'],axis=1)
y_train=df['price']
x_test = test.iloc[:,:]
mmscaler=MinMaxScaler(feature_range=(0,1))
x_train=mmscaler.fit_transform(x_train)

x_test=mmscaler.fit_transform(x_test)
x_train=pd.DataFrame(x_train)
x_test=pd.DataFrame(x_test)  

modelETR = ExtraTreesRegressor(n_estimators=100, max_depth=16, min_samples_leaf=4, n_jobs=-1, random_state=42)
modelETR.fit(x_train, y_train)

y_pred = modelETR.predict(x_test)

df = pd.DataFrame(
    {
        "price": y_pred.tolist()
    }
)

df.to_csv('../result.csv', index=False)