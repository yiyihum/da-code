# Import the relevant libaries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
from matplotlib import pyplot as plt


video = pd.read_csv('../Video_Games_Sales_as_at_22_Dec_2016.csv')
video.head()


video.isnull().any().any()
video = video.dropna(axis=0)

from tabulate import tabulate
tabulate(video.info(), headers='keys', tablefmt='psql')

str_list = [] # empty list to contain columns with strings (words)

# Dataframe contain info only on the 7th Gen consoles
video7th = video[(video['Platform'] == 'Wii') | (video['Platform'] == 'PS3') | (video['Platform'] == 'X360')]
video7th.shape
plt.style.use('dark_background')
genreSales = video7th.groupby(['Genre','Platform']).Global_Sales.sum()
genreSales.unstack().plot(kind='bar',stacked=True,  colormap= 'Reds', 
                          grid=False, figsize=(13,11))
plt.title('Stacked Barplot of Sales per Game Genre')
plt.ylabel('Sales')

plt.show()