import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

uber_df = pd.read_csv("../My Uber Drives - 2016.csv")

# The  shape and size of data 
print(uber_df.shape)
print(uber_df.size)

# Columns names 
uber_df.columns

# Data  type of the columns 
uber_df.dtypes
#get more information about data
uber_df.info()

# Check the missing values 
uber_df.isnull().any()
uber_df[uber_df['END_DATE*'].isnull()]

uber_df.drop(uber_df.index[1155],inplace=True)
uber_df[uber_df.duplicated()]
# Dropping the duplicates values 
uber_df.drop_duplicates(inplace=True)
# Get the initial data with dropping the NA values
uber_df = uber_df.dropna()
#Get the shape of the dataframe after removing the null values
uber_df.shape

plt.figure(figsize=(15,10))
sns.countplot(y="START*",order= pd.value_counts(uber_df['START*']).iloc[:10].index, data=uber_df)
plt.show()

plt.figure(figsize=(15,10))
sns.countplot(y="STOP*",order= pd.value_counts(uber_df['STOP*']).iloc[:10].index, data=uber_df)
plt.show()
