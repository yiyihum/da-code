import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('/workspace/icc hall of fame.csv')

# Count the number of players for each role
role_counts = data['role'].value_counts()

# Create a bar chart
plt.figure(figsize=(12, 6))
role_counts.plot(kind='bar')
plt.xlabel('Player Role')
plt.ylabel('Count')
plt.title('Count of ICC Hall of Fame Inductees by Player Role')

# Save the figure
plt.savefig('/workspace/result.png')
