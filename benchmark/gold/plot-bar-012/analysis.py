import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

student_mat_dataframe = pd.read_csv('../student-mat.csv')

ageList = list(student_mat_dataframe.age.unique())

def categorize_age(age: int):
    if age >= 18:
        return 'adult'
    else:
        return 'teenager'

parentStatusT = []
parentStatusA = []

adultList = ['teenager', 'adult']
student_mat_dataframe['age_category'] = student_mat_dataframe['age'].apply(categorize_age)

for i in adultList:
    x = student_mat_dataframe[student_mat_dataframe.age_category == i]
    parentStatusT.append(sum(x.Pstatus == "T"))
    parentStatusA.append(sum(x.Pstatus == "A"))
    
f,ax = plt.subplots(figsize=(15,10))
sns.barplot(x=adultList,y=parentStatusT,color="red",alpha=0.6,label="Living together")
sns.barplot(x=adultList,y=parentStatusA,color="blue",alpha=0.8,label="Living apart")
ax.legend(loc="upper right",frameon=True)

ax.set(xlabel="Living Together Sum and Living Part Sum ",ylabel="Age",title="Where do children between 15 and 22 live")
plt.savefig('./result.png')