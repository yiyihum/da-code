# import libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandas import Series
import os
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import matplotlib.dates as dates
from datetime import datetime
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
#from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from datetime import timedelta
from statsmodels.tsa.api import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

# load data
FILE_PATH = '../commodity_prices.csv'
df = pd.read_csv(FILE_PATH)

# rename date column to avoid confusion
df.rename(columns={'date':'hist_date'}, inplace=True)

# drop column
df.drop('Unnamed: 0',axis=1,inplace=True)

# drop NULLs (if any)
df.dropna(inplace=True)

# reset index
df.reset_index(drop=True,inplace=True)

# convert DATE to datetime data
df.hist_date = pd.to_datetime(df.hist_date, format='%Y-%m-%d')

# convert other columns to float
for col in df.columns[1:]:
    df[col] = df[col].astype(float)

# creating new index
df.index = df.hist_date

# limit the data points
start = datetime(2000,1,1)
end = datetime(2022,12,31)
df = df[start:end]
    
# extracy year / month / day 
df['year'] = df.hist_date.dt.year
df['month'] = df.hist_date.dt.month
df['day'] = df.hist_date.dt.day

# view
df.head()

# further limiting the data 
start = datetime(2016,1,1)
end = datetime(2022,12,31)
df = df[start:end]

# aggregating the data-points to convert into a monthly series
'''will be taking mean of the monthly data'''
monthly = df.resample('M').mean()   # this is redundant but just to create a new dataset

# view
monthly.head()

# limit the data to fall between the start & end date
start_date = datetime(2020,1,1)
end_date = datetime(2022,12,31)

lim_data = monthly[start_date:end_date]
print(f"Size of the newly limited data: {len(lim_data)}")

# plot the weekly time series - again 
fig, ax = plt.subplots(figsize=(20,8))
#fig = plt.figure(figsize=(20,8))
#plt.plot(weekly['TOTALDEMAND'],".-", label = 'Use')
s = pd.Series(lim_data['coffee_arabica'], index=lim_data.index)

ax.plot_date(lim_data.index, s,'.-')
ax.xaxis.set_minor_locator(dates.MonthLocator(interval=1))
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
#ax.xaxis.grid(True, which="minor")

ax.xaxis.set_major_locator(dates.YearLocator())
ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%Y'))
ax.yaxis.grid()

plt.title('Average Coffee (arabica) Cost', fontsize=16)
#plt.xlabel("Time(Year)", fontsize=12)
plt.ylabel("USD/kg", fontsize=12)
plt.legend(loc = 'best')
plt.tight_layout()
plt.show()


