import numpy as np
import pandas as pd
import scipy.stats as st
pd.set_option('display.max_columns', None)
import math
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
import missingno as msno
from sklearn.preprocessing import StandardScaler
from scipy import stats

import os
for dirname, _, filenames in os.walk('../'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
data = pd.read_csv('../vgsales.csv')
data.head()

drop_row_index = data[data['Year'] > 2015].index
data = data.drop(drop_row_index)

plt.figure(figsize=(15, 10))
sns.countplot(x="Year", data=data, order = data.groupby(by=['Year'])['Name'].count().sort_values(ascending=False).index)
plt.xticks(rotation=90)

plt.show()