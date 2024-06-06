import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_regression
# Ignore Warnings
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('../data.csv')

def make_mi_score(x,y):
    x = x.copy()
    for colname in x.select_dtypes(['object','category']):
        x[colname], _ = x[colname].factorize()
        
    discrete_features = [pd.api.types.is_integer_dtype(t) for t in x.dtypes]
    mi_score = mutual_info_regression(x, y, discrete_features=discrete_features, random_state=42)
    mi_score = pd.Series(mi_score, name='Mutual Information Score', index=x.columns)
    mi_score = mi_score.sort_values(ascending=False)
    return mi_score
X = df.drop(columns=['price'])
y = df[['price']]

mi_score = make_mi_score(X, y)

score = mi_score.sort_values(ascending = True)
width = np.arange(len(score))
ticks = list(score.index)
plt.figure(figsize=(12,6))
plt.bar(width,score)
plt.xticks(width,ticks, rotation=90)
plt.title('Mutual Information Score')
plt.savefig('./result.png')
