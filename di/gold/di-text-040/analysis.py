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

# get our Minimum Qualifications column and convert all of the values to a list
minimum_qualifications = df_job_skills['Minimum Qualifications'].tolist()
# let's join our list to a single string and lower case the letter
miniumum_qualifications_string = "".join(str(v) for v in minimum_qualifications).lower()

years_exp = defaultdict(lambda: 0)

for w in re.findall(r'([0-9]+) year', miniumum_qualifications_string):
     years_exp[w] += 1
        
print(years_exp)

years_exp = sorted(years_exp.items(), key=lambda kv: kv[1], reverse=True)
df_years_exp = pd.DataFrame(years_exp,columns=['Years of experience','Popularity'])
df_years_exp = df_years_exp[::-1] 


# plot
df_years_exp.plot.barh(x='Years of experience',y='Popularity',figsize=(10, 8), legend=False,stacked=True)
# add a suptitle
plt.title("Years of experiences needed for Google Jobs", fontsize=18)
# set xlabel to ""
plt.xlabel("Popularity", fontsize=14)
plt.ylabel("Years of experiences",fontsize=18)
# change xticks fontsize to 14
plt.yticks(fontsize=18)
# finally show the plot
plt.show()
