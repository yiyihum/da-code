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

# Plotting USA born winners using matplotlib
plt.figure(figsize=(10, 5))  
plt.plot(prop_usa_winners['decade'], prop_usa_winners['usa_born_winner'], marker='o', linestyle='-')  
plt.title('Proportion of Nobel Prize Winners Born in the most common birth country of Nobel laureates by Decade')  
plt.xlabel('Decade')  
plt.ylabel('Proportion of USA-born Winners')  
plt.grid(False)  
plt.savefig('result.jpg')  
# plt.show()  
# # Calculating the proportion of female laureates per decade
# nobel['female_winner'] = nobel['sex'] == 'Female'
# prop_female_winners = nobel.groupby(['decade', 'category'], as_index=False)['female_winner'].mean()
# # Find the decade and category with the highest proportion of female laureates
# max_female_decade_category = prop_female_winners[prop_female_winners['female_winner'] == prop_female_winners['female_winner'].max()][['decade', 'category']]
# # Create a dictionary with the decade and category pair
# max_female_dict = {max_female_decade_category['decade'].values[0]: max_female_decade_category['category'].values[0]}
# # Optional: Plotting female winners with % winners on the y-axis
# ax2 = sns.relplot(x='decade', y='female_winner', hue='category', data=prop_female_winners, kind="line")

# # Finding the first woman to win a Nobel Prize
# nobel_women = nobel[nobel['female_winner']]
# min_row = nobel_women[nobel_women['year'] == nobel_women['year'].min()]
# first_woman_name = min_row['full_name'].values[0]
# first_woman_category = min_row['category'].values[0]
# print(f"\n The first woman to win a Nobel Prize was {first_woman_name}, in the category of {first_woman_category}.")
# # Selecting the laureates that have received 2 or more prizes
# counts = nobel['full_name'].value_counts()
# repeats = counts[counts >= 2].index
# repeat_list = list(repeats)

# print("\n The repeat winners are :", repeat_list)