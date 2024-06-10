import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt

import seaborn as sns


import os
if not os.path.exists("../museum_visitors.csv"):
    os.symlink("../data-for-datavis/museum_visitors.csv", "../museum_visitors.csv") 

# Path of the file to read
museum_filepath = "../museum_visitors.csv"

# Fill in the line below to read the file into a variable museum_data
museum_data = pd.read_csv(museum_filepath,index_col="Date",parse_dates = True)

# Run the line below with no changes to check that you've loaded the data correctly
# step_1.check()

# Fill in the line below: How many visitors did the Chinese American Museum 
# receive in July 2018?
ca_museum_jul18 = 2620

# Fill in the line below: In October 2018, how many more visitors did Avila 
# Adobe receive than the Firehouse Museum?
avila_oct18 = 19280 - 4622

# Check your answers
# step_2.check()

# Line plot showing the number of visitors to Avila Adobe over time
plt.figure(figsize=(14,6))
plt.title("Number of visitors to Avila Adobe Museum from 2014 to 2019")
sns.lineplot(data=museum_data['Avila Adobe'],label="Avila Adobe")
plt.xlabel("Date")
plt.savefig('result.png')
# Check your answer
# step_4.a.check()