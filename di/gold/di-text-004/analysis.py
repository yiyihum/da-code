# data
import pandas as pd
import numpy as np
# visualization
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from wordcloud import WordCloud

# read dataframe (drop 3 columns)
df = pd.read_csv('../ds_salaries.csv')
df.drop(df[['salary','salary_currency','Unnamed: 0']],axis=1, inplace=True)
df['experience_level'] = df['experience_level'].replace('EN','Entry-level/Junior')
df['experience_level'] = df['experience_level'].replace('MI','Mid-level/Intermediate')
df['experience_level'] = df['experience_level'].replace('SE','Senior-level/Expert')
df['experience_level'] = df['experience_level'].replace('EX','Executive-level/Director')

ex_level = df['experience_level'].value_counts()

max_count = ex_level.max()
max_level = ex_level[ex_level == max_count].index[0]
max_ratio = max_count / len(df)

print("The most frequent experience level is", max_level, "with a count of", max_count, "and a ratio of", max_ratio)