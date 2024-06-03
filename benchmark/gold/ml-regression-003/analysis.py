import numpy as np      # To use np.arrays
import pandas as pd     # To use dataframes
from sklearn.pipeline import make_pipeline
import warnings
import xgboost as xgb
warnings.filterwarnings("ignore")
from sklearn.preprocessing import RobustScaler

df_store = pd.read_csv('../stores.csv') 
df_train = pd.read_csv('../train.csv')
df_test = pd.read_csv('../test.csv')
df_features = pd.read_csv('../features.csv')
df = df_train.merge(df_features, on=['Store', 'Date'], how='inner').merge(df_store, on=['Store'], how='inner')
df_test = df_test.merge(df_features, on=['Store', 'Date'], how='inner').merge(df_store, on=['Store'], how='inner')
def process_df(df):
    # removing dublicated column
    try:
        df.drop(['IsHoliday_y'], axis=1,inplace=True)
    except:
        pass
    # rename the column
    df.rename(columns={'IsHoliday_x':'IsHoliday'},inplace=True)
    # Super bowl dates in train set
    df.loc[(df['Date'] == '2010-02-12')|(df['Date'] == '2011-02-11')|(df['Date'] == '2012-02-10'),'Super_Bowl'] = True
    df.loc[(df['Date'] != '2010-02-12')&(df['Date'] != '2011-02-11')&(df['Date'] != '2012-02-10'),'Super_Bowl'] = False
    # Labor day dates in train set
    df.loc[(df['Date'] == '2010-09-10')|(df['Date'] == '2011-09-09')|(df['Date'] == '2012-09-07'),'Labor_Day'] = True
    df.loc[(df['Date'] != '2010-09-10')&(df['Date'] != '2011-09-09')&(df['Date'] != '2012-09-07'),'Labor_Day'] = False
    # Thanksgiving dates in train set
    df.loc[(df['Date'] == '2010-11-26')|(df['Date'] == '2011-11-25'),'Thanksgiving'] = True
    df.loc[(df['Date'] != '2010-11-26')&(df['Date'] != '2011-11-25'),'Thanksgiving'] = False
    #Christmas dates in train set
    df.loc[(df['Date'] == '2010-12-31')|(df['Date'] == '2011-12-30'),'Christmas'] = True
    df.loc[(df['Date'] != '2010-12-31')&(df['Date'] != '2011-12-30'),'Christmas'] = False
    df["Date"] = pd.to_datetime(df["Date"]) # convert to datetime
    df['week'] =df['Date'].dt.week
    df['month'] =df['Date'].dt.month 
    df['year'] =df['Date'].dt.year

    df['Date'] = pd.to_datetime(df['Date']) 
    # Encoding the Data
    df_encoded = df.copy() 
    type_group = {'A':1, 'B': 2, 'C': 3}  # changing A,B,C to 1-2-3
    df_encoded['Type'] = df_encoded['Type'].replace(type_group)
    df_encoded['Super_Bowl'] = df_encoded['Super_Bowl'].astype(bool).astype(int) # changing T,F to 0-1
    df_encoded['Thanksgiving'] = df_encoded['Thanksgiving'].astype(bool).astype(int) # changing T,F to 0-1
    df_encoded['Labor_Day'] = df_encoded['Labor_Day'].astype(bool).astype(int) # changing T,F to 0-1
    df_encoded['Christmas'] = df_encoded['Christmas'].astype(bool).astype(int) # changing T,F to 0-1
    df_encoded['IsHoliday'] = df_encoded['IsHoliday'].astype(bool).astype(int) # changing T,F to 0-1
    df_new = df_encoded.copy() # taking the copy of encoded df to keep it original
    # Observation of Interactions between Features
    drop_col = ['Super_Bowl','Labor_Day','Thanksgiving','Christmas']
    df_new.drop(drop_col, axis=1, inplace=True) # dropping columns
    drop_col = ['Temperature','MarkDown4','MarkDown5','CPI','Unemployment']
    df_new.drop(drop_col, axis=1, inplace=True) # dropping columns
    df_new = df_new.sort_values(by='Date', ascending=True) # sorting according to date
    return df_new

target = "Weekly_Sales"
df_train = process_df(df)
df_test = process_df(df_test)

used_cols = [c for c in df_train.columns.to_list() if c not in [target]] # all columns except weekly sales

X_train = df_train[used_cols]
X_test = df_test[used_cols]
y_train = df_train[target]

X_train = X_train.drop(['Date'], axis=1) # dropping date from train
X_test = X_test.drop(['Date'], axis=1) # dropping date from test

scaler = RobustScaler()

params = {
    'objective': 'reg:squarederror',  # 损失函数
    'learning_rate': 1e-3,
    'max_depth': 36,
    'n_estimators': 256,
    'n_job': -1
}

y_test= pd.read_csv('./result.csv')["Weekly_Sales"].tolist()
model = xgb.XGBRegressor(**params)
pipe = make_pipeline(scaler,model)
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
from sklearn import metrics
print('Mean Absolute Error (MAE):', round(metrics.mean_absolute_error(y_test, y_pred),3))  
print('Mean Squared Error (MSE):', round(metrics.mean_squared_error(y_test, y_pred),3))  
print('Root Mean Squared Error (RMSE):', round(np.sqrt(metrics.mean_squared_error(y_test, y_pred)),3))
print('R2_score:', round(metrics.r2_score(y_test, y_pred),6))
print('Root Mean Squared Log Error (RMSLE):', round(np.log(np.sqrt(metrics.mean_squared_error(y_test, y_pred))),3))
