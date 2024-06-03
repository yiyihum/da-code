import numpy as np 
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

df_train=pd.read_csv('../activities.csv')
df_test = pd.read_csv('../activity_test.csv')

# Class Distribution
df_train['Activity'].unique()

# Subject Part
df_train['subject'].unique()
X =pd.DataFrame(df_train.drop(['Activity','subject'],axis=1))
y = df_train.Activity.values.astype(object)
X_test = pd.DataFrame(df_test.drop(['subject'],axis=1))

#Total Number of Continous and Categorical features in the training set
num_cols = X._get_numeric_data().columns
print("Number of numeric features:",num_cols.size)

# Transforming Non numerical Labels into numerical labels
encoder=preprocessing.LabelEncoder()
encoder.fit(y)
y_train=encoder.transform(y)

# Feature Scaling
scaler=StandardScaler()
X_train=scaler.fit_transform(X)
X_test = scaler.transform(X_test)

svc2=SVC(kernel='rbf',C=100.0)
svc2.fit(X_train,y_train)
y_pred = svc2.predict(X_test)

y_pred2= encoder.inverse_transform(y_pred)
print(y_pred2)