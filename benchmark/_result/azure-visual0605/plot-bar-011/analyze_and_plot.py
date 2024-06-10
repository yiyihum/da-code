import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset with ISO-8859-1 encoding to handle potential encoding issues
data = pd.read_csv('/workspace/PoliceKillingsUS.csv', encoding='ISO-8859-1')

# Define the regions as per region.txt
regions = {
    'South': [
        'Alabama', 'Arkansas', 'Florida', 'Georgia', 'Kentucky', 'Louisiana',
        'Maryland', 'Mississippi', 'North Carolina', 'South Carolina',
        'Tennessee', 'Virginia', 'West Virginia'
    ],
    'West': [
        'Alaska', 'California', 'Colorado', 'Hawaii', 'Idaho', 'Montana',
        'Nevada', 'New Mexico', 'Oregon', 'Utah', 'Washington', 'Wyoming'
    ],
    'Northeast': [
        'Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'New Jersey',
        'New York', 'Pennsylvania', 'Rhode Island', 'Vermont', 'District of Columbia'
    ],
    'Midwest': [
        'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Michigan', 'Minnesota',
        'Missouri', 'Nebraska', 'Ohio', 'South Dakota', 'Wisconsin'
    ]
}

# Filter data for those not showing signs of mental illness
no_mental_illness = data[data['signs_of_mental_illness'] == False]

# Count the number of victims without mental illness in each region
region_counts = {region: 0 for region in regions}
for region, states in regions.items():
    region_counts[region] = no_mental_illness[no_mental_illness['state'].isin(states)].shape[0]

# Plot the bar chart
colors = ['#0000FF', '#008000', '#FFA500', '#FF0000']
plt.bar(region_counts.keys(), region_counts.values(), color=colors)
plt.title('Number of Victims Killed by Gunshot without Mental Illness by Region')
plt.xlabel('Region')
plt.ylabel('Number of Victims')
plt.savefig('/workspace/result.png')
