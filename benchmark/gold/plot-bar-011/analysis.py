import pandas as pd
import json
import matplotlib.pyplot as plt

file_path = '../PoliceKillingsUS.csv'
data = pd.read_csv(file_path, encoding="Windows-1252")
states = '../state.json'
with open(states, 'r') as js:
    states = json.load(js)

data =data.dropna(how='any')
data['state'] = [states[state] for state in data['state']]
def Region(x):
    if x=='Alabama':
        return('south')
    elif x=='Alaska':
        return('west')
    elif x=='Arizona':
        return('west')
    elif x=='Arkansas':
        return('south')

    elif x=='California':
        return('west')
    
    elif x=='Colorado':
        return('west')
    
    elif x=='Connecticut':
        return('northeast')
    
    elif x == 'District of Columbia':
        return('northeast')
    
    elif x=='Delaware':
        return('south')
    
    elif x=='Florida':
        return('south')
    elif x=='Georgia':
        return('south')
    elif x=='Hawaii':
        return('west')
    elif x=='Idaho':
        return('west')
    elif x=='Illinois':
        return('Midwest')
    elif x=='Indiana':
        return('Midwest')
    elif x=='Iowa':
        return('Midwest')
    elif x=='Kansas':
        return('Midwest')
    elif x=='Kentucky':
        return('south')
    elif x=='Louisiana':
        return('south')
    elif x=='Maine':
        return('northeast')
    elif x=='Maryland':
        return('south')
    elif x=='Massachusetts':
        return('northeast')
    elif x=='Michigan':
        return('Midwest')
    elif x=='Minnesota':
        return('Midwest')
    elif x=='Mississippi':
        return('south')
    elif x=='Missouri':
        return('Midwest')
    elif x=='Montana':
        return('west')
    elif x=='Nebraska':
        return('Midwest')
    elif x=='Nevada':
        return('west')
    elif x=='New Hampshire':
        return('northeast')
    elif x=='New Jersey':
        return('northeast')
    elif x=='New Mexico':
        return('west')
    elif x=='New York':
        return('northeast')
    elif x=='North Carolina':
        return('south')
    elif x=='North Dakota':
        return('Midwest')
    elif x=='Ohio':
        return('Midwest')
    elif x=='Oklahoma':
        return('south')
    elif x=='Oregon':
        return('west')
    elif x=='Pennsylvania':
        return('northeast')
    elif x=='Rhode Island':
        return('northeast')
    elif x=='South Carolina':
        return('south')
    elif x=='South Dakota':
        return('Midwest')
    elif x=='Tennessee':
        return('south')
    elif x=='Texas':
        return('south')
    elif x=='Utah':
        return('west')
    elif x=='Vermont':
        return('northeast')
    elif x=='Virginia':
        return('south')
    elif x=='Washington':
        return('west')
    elif x=='West Virginia':
        return('south')
    elif x=='Wisconsin':
        return('Midwest')
    elif x=='Wyoming':
        return('west')
data['Region']=data['state'].apply(Region)

def count_victims(region, df):
    region_df = df[df['Region'] == region]
    filtered_df = region_df[(region_df['signs_of_mental_illness'] == False)]
    num_victims = filtered_df.shape[0]
    return num_victims

regions = ['south', 'west', 'northeast', 'Midwest']
num_victims = [count_victims(region, data) for region in regions]

plt.bar(regions, num_victims, color=['blue', 'green', 'orange', 'red'])
plt.xlabel('Region')
plt.ylabel('Number of Victims')
plt.title('Number of Victims Killed by Gunshot without Mental Illness by Region')
plt.savefig('./result.png')