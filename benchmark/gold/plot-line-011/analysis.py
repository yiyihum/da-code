# Loading in required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # 导入matplotlib.pyplot

# Read in the Nobel Prize data
nobel = pd.read_csv('../nobel.csv')

# Store and display the most commonly awarded gender and birth country in requested variables
top_gender = nobel['sex'].value_counts().index[0]
top_country = nobel['birth_country'].value_counts().index[0]

# Calculate the proportion of USA born winners per decade
nobel['usa_born_winner'] = nobel['birth_country'] == top_country
nobel['decade'] = (np.floor(nobel['year'] / 10) * 10).astype(int)
prop_usa_winners = nobel.groupby('decade', as_index=False)['usa_born_winner'].mean()

# Identify the decade with the highest proportion of US-born winners
max_decade_usa = prop_usa_winners[prop_usa_winners['usa_born_winner'] == prop_usa_winners['usa_born_winner'].max()]


import matplotlib.pyplot as plt

# Calculating the proportion of male laureates per decade
nobel['male_winner'] = nobel['sex'] == 'Male'
prop_male_winners = nobel.groupby(['decade', 'category'], as_index=False)['male_winner'].mean()

# Find the decade and category with the highest proportion of male laureates
max_male_decade_category = prop_male_winners[prop_male_winners['male_winner'] == prop_male_winners['male_winner'].max()][['decade', 'category']]
# Create a dictionary with the decade and category pair
max_male_dict = {max_male_decade_category['decade'].values[0]: max_male_decade_category['category'].values[0]}

# Optional: Plotting male winners with % winners on the y-axis using matplotlib
plt.figure(figsize=(10, 6))

categories = prop_male_winners['category'].unique()
for category in categories:
    category_data = prop_male_winners[prop_male_winners['category'] == category]
    plt.plot(category_data['decade'], category_data['male_winner'] * 100, marker='o', label=category)

plt.title('Proportion of Top Gender Nobel Prize Winners by Decade and Category')
plt.xlabel('Decade')
plt.ylabel('Percentage of Top Gender Winners')
plt.legend()
plt.savefig('result.jpg')

# # Finding the first woman to win a Nobel Prize
# nobel_women = nobel[nobel['male_winner']]
# min_row = nobel_women[nobel_women['year'] == nobel_women['year'].min()]
# first_woman_name = min_row['full_name'].values[0]
# first_woman_category = min_row['category'].values[0]
# print(f"\n The first woman to win a Nobel Prize was {first_woman_name}, in the category of {first_woman_category}.")
# # Selecting the laureates that have received 2 or more prizes
# counts = nobel['full_name'].value_counts()
# repeats = counts[counts >= 2].index
# repeat_list = list(repeats)

# print("\n The repeat winners are :", repeat_list)