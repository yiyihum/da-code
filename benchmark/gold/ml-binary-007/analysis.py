import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import KBinsDiscretizer

df = pd.read_csv('../customer_churn_dataset-testing-master.csv')
dt = pd.read_csv('../customer_churn_dataset-training-master.csv')
df.dropna(inplace = True)
dt.dropna(inplace = True)

def cat_to_num(df, col, cat1, cat2, cat3 = None):
    df.loc[df[col] == cat1, col] = 0
    df.loc[df[col] == cat2, col] = 1
    df.loc[df[col] == cat3, col] = 2

cat_to_num(df, 'Subscription Type', 'Standard' , 'Basic', 'Premium')
cat_to_num(df, 'Contract Length', 'Monthly' , 'Quarterly', 'Annual')
cat_to_num(df, 'Gender', 'Male' , 'Female')

cat_to_num(dt, 'Subscription Type', 'Standard' , 'Basic', 'Premium')
cat_to_num(dt, 'Contract Length', 'Monthly' , 'Quarterly', 'Annual')
cat_to_num(dt, 'Gender', 'Male' , 'Female')

trans = KBinsDiscretizer(n_bins=7,encode='ordinal',strategy='kmeans')

def transform(df, cols, trans):
    for col in cols:
        trf = ColumnTransformer(
            transformers=[(col, trans, [col])]
        )
        trf_data = trf.fit_transform(df)
        df[col] = trf_data[:, 0] 
    return df

trf_df = transform(df, ['Support Calls','Tenure','Usage Frequency', 'Total Spend', 'Last Interaction'], trans)
trf_dt = transform(df, ['Support Calls','Tenure','Usage Frequency', 'Total Spend', 'Last Interaction'], trans)

trf_df.set_index('CustomerID', inplace = True)

x_train = trf_df.iloc[:,:-1].values
y_train = trf_df.iloc[:,-1].values
x_test = trf_dt.iloc[:,:].values

rfc = GradientBoostingClassifier(n_estimators=50, max_depth = 10)
rfc.fit(x_train, y_train)
y_pred = rfc.predict(x_test)

df = pd.DataFrame(y_pred, columns=['result'])
df.to_csv('../result.csv', index=False)
