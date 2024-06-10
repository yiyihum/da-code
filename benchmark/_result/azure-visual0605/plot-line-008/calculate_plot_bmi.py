import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/all_seasons.csv')

# Convert height from centimeters to meters and calculate BMI
df['player_height_m'] = df['player_height'] / 100
df['BMI'] = df['player_weight'] / (df['player_height_m']**2)

# Calculate the average BMI for each season
average_bmi_per_season = df.groupby('season')['BMI'].mean().reset_index()

# Plotting the average BMI per season
plt.figure(figsize=(16, 8))
plt.plot(average_bmi_per_season['season'], average_bmi_per_season['BMI'], color='#17408b')
plt.title('Average BMI Each Season')
plt.xlabel('Season')
plt.ylabel('BMI')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/workspace/result.png')
