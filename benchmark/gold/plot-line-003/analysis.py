import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('../fake.csv')
# rename first column 'uuid' to 'id'
df.rename(columns={'uuid':'id'},inplace=True)

#transform types of published and crawled columns from object to datetime
df['published']=pd.to_datetime(df['published'],utc=True)
df['crawled']=pd.to_datetime(df['crawled'],utc=True)
# add to column 'crawled_by_day' by transform column "crawled"
df.insert(8,'crawled_by_day',pd.to_datetime(df['crawled'],utc=True).dt.strftime('%Y-%m-%d'))
# add to column 'published_by_day' by transform column "published"
df.insert(4,'published_by_day',pd.to_datetime(df['published'],utc=True).dt.strftime('%Y-%m-%d'))

plt.figure(figsize=(30,7))
plt.xticks(rotation=75)
sns.lineplot(x='published_by_day',y='spam_score',data=df,ci=None)
sns.lineplot(x='crawled_by_day',y='spam_score',data=df,ci=None)
plt.xlabel('day');
