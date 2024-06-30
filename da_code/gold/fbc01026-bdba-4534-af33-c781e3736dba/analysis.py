import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from matplotlib.lines import Line2D
from warnings import filterwarnings

df = pd.read_csv('../bestsellers with categories.csv')
df.loc[df['Author']=='J. K. Rowling','Author']='J.K. Rowling'
df.loc[df['Author']=='George R. R. Martin','Author']='George R.R. Martin'
IQR_r = df['Reviews'].quantile(0.75)-df['Reviews'].quantile(0.25)

upper_limit = df['Reviews'].quantile(0.75)+IQR_r*1.5
lower_limit = df['Reviews'].quantile(0.75)-IQR_r*1.5

ex_lower_limit = df['Reviews'].quantile(0.75)-IQR_r*3
ex_upper_limit = df['Reviews'].quantile(0.75)+IQR_r*3

print('Outlier\'s range :\t',[lower_limit,upper_limit])
print('Extreme Outlier\'s range:',[ex_lower_limit,ex_upper_limit])
