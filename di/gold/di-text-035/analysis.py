# for manupilating data
import pandas  as pd 
import numpy as np

# for visualizations
import matplotlib.pyplot as plt
import seaborn as sns
from colorama import Fore
sns.set_style("darkgrid")

df = pd.read_csv('../train.csv') # this a data that i will train on it
df.head()

df.duplicated().any()
# the next 5 lines define the default font sizes
plt.rc('font', size=14)
plt.rc('axes', labelsize=14, titlesize=18)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)

df.drop(['Unnamed: 0','id'],axis = 1).hist(bins=22, figsize=(20, 18), grid = True)
plt.show()

plt.figure(figsize = (10,5))

df["satisfaction"].replace({"satisfied": 1, "neutral or dissatisfied": 0}, inplace = True)
df_dummies = pd.get_dummies(df)

df_dummies.corr()['satisfaction'].sort_values(ascending = False).plot(kind = 'bar')

plt.show()

print(df_dummies.corr()['satisfaction'].sort_values(ascending = False))
