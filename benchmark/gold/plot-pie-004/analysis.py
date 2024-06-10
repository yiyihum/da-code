import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # visualize
import matplotlib.pyplot as plt


data = pd.read_csv('../student-mat.csv')
data['Dalc'] = data['Dalc'] + data['Walc']
list = []
for i in range(11):
    list.append(len(data[data.Dalc == i]))

labels = ['2','3','4','5','6','7','8','9','10']
colors = ['lime','blue','orange','cyan','grey','purple','brown','red','darksalmon']
explode = [0,0,0,0,0,0,0,0,0]
sizes = []
for i in range(2,11):
    sizes.append(sum(data[data.Dalc == i].G3))
total_grade = sum(sizes)
average = total_grade/float(len(data))
plt.pie(sizes,explode=explode,colors=colors,labels=labels,autopct = '%1.1f%%')
plt.axis('equal')
plt.title('Final Grade')
plt.xlabel('Students grade distribution according to weekly alcohol consumption')

plt.savefig('result.png')
