import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import seaborn as sns
from itertools import cycle

df = pd.read_csv("../diabetes_012_health_indicators_BRFSS2015.csv")

df['Diabetes_012_str'] = df['Diabetes_012'].replace({0.0:'Healthy', 1.0:'Pre-diabetic', 2.0:'Diabetic'})

countHealthy = len(df[df.Diabetes_012 == 0])
countHavePreDiabetic = len(df[df.Diabetes_012 == 1])
countDiabteic = len(df[df.Diabetes_012 == 2])
print("Percentage of Patients Are Healthy: {:.2f}%".format((countHealthy / (len(df.Diabetes_012))*100)))
print("Percentage of Patients Have Pre-Diabetic: {:.2f}%".format((countHavePreDiabetic / (len(df.Diabetes_012))*100)))
print("Percentage of Patients Have Diabetic: {:.2f}%".format((countDiabteic / (len(df.Diabetes_012))*100)))


fig1, ax1 = plt.subplots(figsize=(8,8))
labels = ['Healthy', 'Diabetic', 'Pre-Diabetic']
sizes = df['Diabetes_012'].value_counts()
colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] 
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=180)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Proportion of Different Diabetes States')
plt.legend()
plt.savefig("result.png")
plt.show()