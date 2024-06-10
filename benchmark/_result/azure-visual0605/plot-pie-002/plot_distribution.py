import pandas as pd
import matplotlib.pyplot as plt

# Load the deliveries dataset
deliveries = pd.read_csv('deliveries.csv')

# Filter the deliveries for V Kohli
kohli_deliveries = deliveries[deliveries['batsman'] == 'V Kohli']

# Count the number of occurrences of each run type (1-6)
run_counts = kohli_deliveries['batsman_runs'].value_counts().sort_index()

# Filter out run types that are not 1-6
run_counts = run_counts[run_counts.index.isin([1, 2, 3, 4, 5, 6])]

# Plot the distribution of runs in a pie chart
plt.figure(figsize=(8, 8))
plt.pie(run_counts, labels=run_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Batsman Runs for V Kohli')
plt.legend(title='Runs')
plt.savefig('distribution.png')
plt.close()
