import pandas as pd
# numpy for numeric operations
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
# use ggplot style
plt.style.use('ggplot')
# seaborn for beautiful visualizations
import seaborn as sns
# regualar expression
import re

# read the data set using pandas .read_csv() method
df_job_skills = pd.read_csv('../job_skills.csv')
# print the top 5 row from the dataframe
df_job_skills.head()

# most popular language list 
programing_language_list = ['python', 'java', 'c++', 'php', 'javascript', 'objective-c', 'ruby', 'perl','c','c#', 'sql','kotlin']
# get our Minimum Qualifications column and convert all of the values to a list
minimum_qualifications = df_job_skills['Minimum Qualifications'].tolist()
# let's join our list to a single string and lower case the letter
miniumum_qualifications_string = "".join(str(v) for v in minimum_qualifications).lower()

# find out which language occurs in most in minimum Qualifications string
wordcount = dict((x,0) for x in programing_language_list)
for w in re.findall(r"[\w'+#-]+|[.!?;’]", miniumum_qualifications_string):
    if w in wordcount:
        wordcount[w] += 1
# print
print(wordcount)

# sort the dict
programming_language_popularity = sorted(wordcount.items(), key=lambda kv: kv[1], reverse=True)

# make a new dataframe using programming_language_popularity for easy use cases
df_popular_programming_lang = pd.DataFrame(programming_language_popularity,columns=['Language','Popularity'])
# Capitalize each programming language first letter
df_popular_programming_lang['Language'] = df_popular_programming_lang.Language.str.capitalize()
df_popular_programming_lang = df_popular_programming_lang[::-1]

# plot
df_popular_programming_lang.plot.barh(x='Language',y='Popularity',figsize=(10,8), legend=False)
# add a suptitle
plt.suptitle("Programming Languages popularity at Google Jobs", fontsize=18)
# set xlabel to ""
plt.xlabel("")
# change xticks fontsize to 14
plt.yticks(fontsize=14)
# finally show the plot
plt.show()




