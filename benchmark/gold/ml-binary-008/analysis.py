import pandas as pd
import warnings
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
#ML models
from sklearn.tree import DecisionTreeClassifier
#warning hadle
warnings.filterwarnings("ignore")
#path for the training set
tr_path = "../train_u6lujuX_CVtuZ9i.csv"
te_path = '../test.csv'
tr_df = pd.read_csv(tr_path)
te_df = pd.read_csv(te_path)

tr_df.drop('Loan_ID',axis=1,inplace=True)
te_df.drop('Loan_ID',axis=1,inplace=True)

null_cols = ['Credit_History', 'Self_Employed', 'LoanAmount','Dependents', 'Loan_Amount_Term', 'Gender', 'Married']

for col in null_cols:
    tr_df[col] = tr_df[col].fillna(
    tr_df[col].dropna().mode().values[0] )   
    te_df[col] = te_df[col].fillna(
        te_df[col].dropna().mode().values[0] )

to_numeric = {'Male': 1, 'Female': 2,
'Yes': 1, 'No': 2,
'Graduate': 1, 'Not Graduate': 2,
'Urban': 3, 'Semiurban': 2,'Rural': 1,
'Y': 1, 'N': 0,
'3+': 3}

# adding the new numeric values from the to_numeric variable to both datasets
tr_df = tr_df.applymap(lambda lable: to_numeric.get(lable) if lable in to_numeric else lable)
te_df = te_df.applymap(lambda lable: to_numeric.get(lable) if lable in to_numeric else lable)
# convertind the Dependents column
Dependents_ = pd.to_numeric(tr_df.Dependents)
Dependents_test = pd.to_numeric(te_df.Dependents)

# dropping the previous Dependents column
tr_df.drop(['Dependents'], axis = 1, inplace = True)
te_df.drop(['Dependents'], axis = 1, inplace = True)

# concatination of the new Dependents column with both datasets
tr_df = pd.concat([tr_df, Dependents_], axis = 1)
te_df = pd.concat([te_df, Dependents_test], axis = 1)

y_train = tr_df['Loan_Status']
X_train = tr_df.drop('Loan_Status', axis = 1)
X_test = te_df.iloc[:, :]

DT = DecisionTreeClassifier(max_depth=6, random_state=42)
DT.fit(X_train, y_train)

y_predict = DT.predict(X_test)

id2label = {0: 'N', 1: 'Y'}
df = pd.DataFrame([id2label[id] for id in y_predict.tolist()], columns=['Loan_Status'])
df.to_csv('./result.csv', index=False)




