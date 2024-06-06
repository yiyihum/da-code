import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # data visualization
import seaborn as sns # statistical data visualization
import warnings # handle warning messages
warnings.filterwarnings('ignore') # Ignore warning messages

df = pd.read_csv('../Song.csv')

# Rename columns to lowercase
df.columns = df.columns.str.lower()

# Rename the 'Radio Plays' column to 'radio_plays'
df.rename(columns={'radio plays': 'radio_plays'}, inplace=True)

# Checking the duplicate values in the data
duplicate_values = df.duplicated().sum()

# List of metrics to plot
metrics = ['sales']  # Add more metrics as needed

# Set the style of seaborn
sns.set_style("whitegrid")
for metric in metrics:
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Obtain the top ten artists based on the current metric
    top_ten = df.groupby('artist')[metric].agg('mean' if metric == 'rating' else 'sum').nlargest(10).reset_index()
    
    # Plot the top ten artists with vertical bars
    sns.barplot(x='artist', y=metric, data=top_ten, ax=ax, palette='viridis' if metric == 'sales' else 'magma')
    ax.set_title(f'Top Ten Artists Based on {metric.capitalize()}')
    ax.set_xlabel('Artist')
    ax.set_ylabel(f'Total {metric.capitalize()}' if metric == 'sales' else f'Average {metric.capitalize()}')

    plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility
    plt.tight_layout()
    
    # Save the figure
    fig.savefig(f'{metric}.jpg')

plt.close('all') # Close all the figures