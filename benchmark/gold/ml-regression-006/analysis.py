import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.preprocessing import LabelEncoder 

df = pd.read_csv("../Output.csv", sep=';', low_memory=False)
test = pd.read_csv("../test.csv", low_memory=False)
df.drop(columns=['Sets URL', 'Part URL'], axis=1, inplace=True)
test.drop(columns=['Sets URL', 'Part URL'], axis=1, inplace=True)
df.dropna(axis=0, inplace=True)

df['Star rating'] = df['Star rating'].apply(lambda x: x.replace(',', '.'))
numeric_features = ['Set Price', 'Number of reviews', 'Star rating', 'year']

for feature in numeric_features: 
    df[feature] = pd.to_numeric(df[feature].apply(lambda x: x.replace(",","") if type(x) not in (int, float) else x))
    if feature != 'Star rating':
        test[feature] = pd.to_numeric(df[feature].apply(lambda x: x.replace(",","") if type(x) not in (int, float) else x))

encoders = {}
text_features = [feature for feature in df.columns if feature not in numeric_features]
# print(text_features)

for feature in text_features: 
    encoders[feature] = LabelEncoder()
    df[feature] = encoders[feature].fit_transform(df[feature])
    test[feature] = encoders[feature].fit_transform(test[feature])

corr = df.corr()
corr = corr["Star rating"]
threshold = 0.005

low_corr_features = corr[abs(corr) < threshold].index
df_filtered = df.drop(low_corr_features, axis=1)
test_filtered = test.drop(low_corr_features, axis=1)

df_filtered.drop_duplicates(inplace=True)

# splitting data
X_train = df_filtered.drop('Star rating', axis=1)
y_train = df_filtered['Star rating']
X_test = test_filtered

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

pipe1 = Pipeline([
    ("scaler", StandardScaler()),
    ("regressor", RandomForestRegressor(n_estimators=256, max_depth=16, max_features='sqrt',  n_jobs = -1))
])

pipe1.fit(X_train, y_train)
y_pred = pipe1.predict(X_test)

result = pd.DataFrame(data=y_pred.tolist(), columns=['Star rating'])

result.to_csv('../result.csv', index=False)

