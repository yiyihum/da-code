import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/appstore_games.csv')

# Correct the date parsing with the appropriate format
df['Current Version Release Date'] = pd.to_datetime(df['Current Version Release Date'], format='%d/%m/%Y', errors='coerce')
df['Original Release Date'] = pd.to_datetime(df['Original Release Date'], format='%d/%m/%Y', errors='coerce')

# Filter out games with user ratings less than 200 and update time less than 6 months
cutoff_date = pd.to_datetime('2019-06-30')  # Assuming the dataset was collected on 2019-12-31
df = df[(df['User Rating Count'] >= 200) & (df['Current Version Release Date'] <= cutoff_date)]

# Categorize games into the four main types
conditions = [
    (df['Genres'].str.contains('Puzzle') | df['Genres'].str.contains('Board')),
    (df['Genres'].str.contains('Action')),
    (df['Genres'].str.contains('Adventure') | df['Genres'].str.contains('Role')),
    (df['Genres'].str.contains('Family') | df['Genres'].str.contains('Education'))
]
choices = ['Puzzle', 'Action', 'Adventure', 'Family']
df['Main Genre'] = np.select(conditions, choices, default='Other')

# Filter out games that do not fit into the four main types
df = df[df['Main Genre'] != 'Other']

# Convert game size from bytes to MB
df['Size MB'] = df['Size'] / (1024 * 1024)

# Group by year and main genre, then calculate the average size
df['Release Year'] = df['Original Release Date'].dt.year
avg_size_per_year = df.groupby(['Release Year', 'Main Genre'])['Size MB'].mean().unstack()

# Plot the results
plt.figure(figsize=(16, 6))
colors = ['darkblue', 'green', 'red', 'orange']
avg_size_per_year.plot(kind='line', color=colors, title='Game size changes over 12 years by Genre')
plt.xlabel('Year')
plt.ylabel('Game Size in MB')
plt.savefig('/workspace/result.png')
