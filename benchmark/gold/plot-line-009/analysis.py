import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

temp_data = pd.read_csv('../city_temperature.csv',
    dtype={'Region': 'str', 'Country': 'str', 'State': 'str', 'City': 'str', 
    'Month': 'int', 'Day': 'int', 'Year': 'int', 'AvgTemperature': 'float'}, encoding  = 'utf-8')

temp_data = temp_data.drop(['State'], axis = 1)
temp_data = temp_data.drop_duplicates()

temp_data = temp_data[temp_data['Day'] > 0]
temp_data = temp_data[temp_data['Year'] > 1994]
temp_data = temp_data[temp_data['Year'] < 2020]
temp_data = temp_data[temp_data['AvgTemperature'] > -70]

temp_data['AvgTemperature'] = (temp_data['AvgTemperature'] - 32)*(5/9)
temp_data['Date'] = pd.to_datetime(temp_data[['Year','Month','Day']])

kar_data = temp_data[temp_data['City'] == 'Karachi']
Isl_data = temp_data[temp_data['City'] == 'Islamabad']

plt.figure(figsize=(12, 8))

plt.plot(kar_data['Date'], kar_data['AvgTemperature'], 'g', label='Karachi')
plt.plot(Isl_data['Date'], Isl_data['AvgTemperature'], 'r', label='Islamabad')

plt.legend()
plt.title('Average Temperature Comparison between Karachi and Islamabad')
plt.xlabel('Year')
plt.ylabel('AvgTemperature')

plt.show()