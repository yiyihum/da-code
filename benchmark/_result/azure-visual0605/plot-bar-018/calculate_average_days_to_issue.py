import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/Building_Permits.csv')

# Convert 'Filed Date' to datetime and extract the day of the week
df['Filed Date'] = pd.to_datetime(df['Filed Date'])
df['Weekday'] = df['Filed Date'].dt.day_name()

# Group by the day of the week and calculate the average 'Days_to_Issue'
average_days_to_issue = df.groupby('Weekday')['Days_to_Issue'].mean().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
])

# Plot the results in a bar chart
plt.figure(figsize=(12, 6))
average_days_to_issue.plot(kind='bar', color='skyblue')
plt.title('Average Days to Issue by Weekday')
plt.xlabel('Weekday')
plt.ylabel('Average Days to Issue')
plt.savefig('/workspace/result.png')
plt.close()
