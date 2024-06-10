import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the dataset
df = pd.read_csv('/workspace/appstore_games.csv')

# Convert 'Original Release Date' and 'Current Version Release Date' to datetime
df['Original Release Date'] = pd.to_datetime(df['Original Release Date'], format='%d/%m/%Y')
df['Current Version Release Date'] = pd.to_datetime(df['Current Version Release Date'], format='%d/%m/%Y')

# Calculate the number of days since the original release date
df['Days Since Release'] = (df['Current Version Release Date'] - df['Original Release Date']).dt.days

# Filter out games with user ratings less than 200
df_filtered = df[df['User Rating Count'] >= 200]

# Create a scatter plot
plt.figure(figsize=(16, 6))
plt.scatter(df_filtered['Days Since Release'], df_filtered['User Rating Count'], color='blue')

# Label the axes
plt.xlabel('Updated version date since release (days)')
plt.ylabel('User Rating count')

# Save the plot
plt.savefig('/workspace/result.png')
