import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("../heart.csv")
test = pd.read_csv("../test.csv")

cat_cols = ['sex', 'exng', 'caa', 'cp', 'fbs', 'restecg', 'slp', 'thall']
con_cols = ["age", "trtbps", "chol", "thalachh", "oldpeak"]
target_col = ["output"]

df1 = df.copy()
df1 = pd.get_dummies(df1, columns=cat_cols, drop_first=True)
test = pd.get_dummies(test, columns=cat_cols, drop_first=True)

X = df1.drop(['output'], axis=1)
y = df1['output'] 

scaler = RobustScaler()

X[con_cols] = scaler.fit_transform(X[con_cols])
test[con_cols] = scaler.fit_transform(test[con_cols])

logreg = LogisticRegression()
logreg.fit(X, y)

y_pred_proba = logreg.predict_proba(test)

y_pred = np.argmax(y_pred_proba, axis=1)

y_pred_df = pd.DataFrame(y_pred, columns=['output'])
y_pred_df.to_csv("../result.csv", index=False)
