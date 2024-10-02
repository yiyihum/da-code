import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import warnings
warnings.filterwarnings('ignore')

df=pd.read_csv('../Economy_Indicators.csv')
df.head()
df.info()

df=df.replace('           NA',np.nan,regex=True)
df['GDP Quarter-over-Quarterr'] = df['GDP Quarter-over-Quarterr'].astype(float)
df['Interest Rate'] = df['Interest Rate'].astype(float)
df=df.drop('Country', axis=1)

col=["GDP", "GDP Year-over-Year", "GDP Quarter-over-Quarterr",
       "Interest Rate", "Inflation Rate", "Jobless Rate", "Gov. Budget",
       "Debt/GDP", "Current Account", "Population"]
sns.heatmap(df.corr(),annot=True, cbar=False, cmap='Blues', fmt='.4f')

plt.show()