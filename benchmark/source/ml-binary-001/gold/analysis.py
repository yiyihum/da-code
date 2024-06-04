import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from collections import Counter
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold



df_train = pd.read_csv('../onlinefoods.csv')
df_test = pd.read_csv('../test.csv')
df_train = df_train.drop('Unnamed: 12',axis=1)
df_test = df_test.drop('Unnamed: 12',axis=1)

y_test = pd.read_csv('./result.csv')


label_encoder = LabelEncoder()
df_train['Educational Qualifications'] = label_encoder.fit_transform(df_train['Educational Qualifications'])
df_test['Educational Qualifications'] = label_encoder.fit_transform(df_test['Educational Qualifications'])

df_train['Feedback'] = label_encoder.fit_transform(df_train['Feedback'])
y_test['result'] = label_encoder.fit_transform(y_test['result'])

df_encoded_train = pd.get_dummies(df_train, columns=['Gender', 'Marital Status', 'Occupation', 'Monthly Income', 'Output'])
df_encoded_test = pd.get_dummies(df_test, columns=['Gender', 'Marital Status', 'Occupation', 'Monthly Income', 'Output'])

df_train = df_encoded_train.astype('int')
df_test = df_encoded_test.astype('int')

X_train = df_train.drop('Feedback',axis=1)
X_test = df_test
y_train = df_train['Feedback']

y_test = y_test['result']

Scaler_X = StandardScaler()
X_train = Scaler_X.fit_transform(X_train)
X_test = Scaler_X.transform(X_test)

counter = Counter(y_train)
# oversampling train dataset using smote
smt= SMOTE()
X_train_sm,y_train_sm = smt.fit_resample(X_train,y_train)

estimators = [2,10,30,50,100]
# Maximum number of depth in each tree:
max_depth = [i for i in range(5,16,2)]
# Minimum number of samples to consider to split a node:
min_samples_split = [2, 5, 10, 15, 20, 50, 100]
# Minimum number of samples to consider at each leaf node:
min_samples_leaf = [1, 2, 5]

tree_model = DecisionTreeClassifier()

tree_param_grid = {
    'max_depth': max_depth,
    'min_samples_split': min_samples_split,
    'min_samples_leaf': min_samples_leaf
}

cv = StratifiedKFold(n_splits=5, random_state=30, shuffle=True)
clf_DT = RandomizedSearchCV(tree_model, tree_param_grid, cv=cv, scoring='roc_auc', n_jobs=-1, verbose=2)
clf_DT.fit(X_train, y_train)
clf_DT.best_estimator_
y_pred=clf_DT.predict(X_test)

map = {
    0: 'Negative',
    1: 'Positive'
}
result = pd.DataFrame(
    {
        "result": [map[i] for i in y_pred]
    }
)


result.to_csv('../result.csv', index=False)
