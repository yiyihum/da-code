import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/nobel.csv')

# Extract the decade from the 'year' column
df['decade'] = (df['year'] // 10) * 10

# Group by 'decade' and 'category' and count the number of male and female laureates
gender_counts = df.groupby(['decade', 'category', 'sex']).size().unstack(fill_value=0)

# Determine the gender with the most laureates for each group
top_gender_counts = gender_counts.idxmax(axis=1)

# Calculate the percentage of the top gender's laureates for each group
top_gender_percentages = gender_counts.max(axis=1) / gender_counts.sum(axis=1) * 100

# Prepare the data for plotting
plot_data = top_gender_percentages.unstack('category')

# Plot the results
plt.figure(figsize=(10, 6))
for category in plot_data.columns:
    plt.plot(plot_data.index, plot_data[category], label=category)

plt.title('Proportion of Top Gender Nobel Prize Winners by Decade and Category')
plt.xlabel('Decade')
plt.ylabel('Percentage of Top Gender Winners')
plt.legend()
plt.savefig('/workspace/result.jpg')
