import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns


uber_df = pd.read_csv("../My Uber Drives - 2016.csv")
# First 5 records 
uber_df.head()
# Last 5 records 
uber_df.tail()
# The  shape and size of data 
print(uber_df.shape)
print(uber_df.size)
# Columns names 
uber_df.columns

uber_df[uber_df['END_DATE*'].isnull()]
uber_df.drop(uber_df.index[1155],inplace=True)
#Duplicated Records needs to be removed 
uber_df[uber_df.duplicated()]


#Find out most farthest start and stop pair -top10
#Dropping Unknown Location Value
uber_df2 = uber_df[uber_df['START*']!= 'Unknown Location']
uber_df2 = uber_df2[uber_df2['STOP*']!= 'Unknown Location']

uber_df2.groupby(['START*','STOP*'])['MILES*'].sum().sort_values(ascending=False).head(10)

m = {}
for i in uber_df['MILES*']:
    for i in uber_df['MILES*']:
        if i < 10:
            m.setdefault(i,'0-10 miles')
        elif i >= 10 and i < 20:
            m.setdefault(i,'10-20 miles')
        elif i >= 20 and i < 30:
            m.setdefault(i,'20-30 miles')
        elif i >= 30 and i < 40:
            m.setdefault(i,'30-40 miles')
        elif i >= 40 and i < 50:
            m.setdefault(i,'40-50 miles')
        else:
            m.setdefault(i,'Above 50 miles')
            
uber_df['MILES_BUCKET*'] = uber_df['MILES*'].map(m)

print(type(uber_df['MILES_BUCKET*']))

plt.figure(figsize=(10,6))
sns.countplot(x='MILES_BUCKET*', data=uber_df, palette='Set1', 
              order=uber_df['MILES_BUCKET*'].value_counts().index)
plt.show()
