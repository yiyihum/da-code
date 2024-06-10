import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('student-mat.csv')

# Calculate the total weekly alcohol consumption
df['TotalAlc'] = df['Dalc'] + df['Walc']

# Filter the alcohol consumption levels from 2 to 10
df_filtered = df[(df['TotalAlc'] >= 2) & (df['TotalAlc'] <= 10)]

# Group by the total weekly alcohol consumption and count the number of students
alc_counts = df_filtered['TotalAlc'].value_counts().sort_index()

# Define the colors for the pie chart
colors = ['lime', 'blue', 'orange', 'cyan', 'grey', 'purple', 'brown', 'red', 'darksalmon']

# Create the pie chart
plt.figure(figsize=(10, 8))
plt.pie(alc_counts, labels=alc_counts.index, autopct='%1.1f%%', colors=colors)
plt.title('Final Grade')
plt.xlabel('Students grade distribution according to weekly alcohol consumption')

# Save the pie chart as result.png
plt.savefig('result.png')
