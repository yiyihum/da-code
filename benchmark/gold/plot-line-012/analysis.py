import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt 
import seaborn as sns
df = pd.read_csv('Plot-line\\Plot-line-3\\MyTransaction.csv')

# only the first row has null values so i am droping it
df.dropna(inplace= True)

df.drop(columns=['RefNo','Date.1'], inplace= True)
# Renaming the columns for easier use 
df.rename(columns={'Date':'date',
                   'Category':'category',
                   'Withdrawal':'withdrawal',
                   'Deposit':'deposit',
                   'Balance':'balance'
                  }, inplace = True)

df['date'] = pd.to_datetime(df['date'] , format = "mixed",dayfirst=True)

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df.drop(columns=['date'],inplace=True)

df = df[df['year'] != 2024]

avg_monthly_withdrawal_deposit = df.groupby(['month']).agg({'withdrawal': 'mean', 'deposit': 'mean'})
avg_monthly_withdrawal_deposit = avg_monthly_withdrawal_deposit.reset_index()

plt.plot(avg_monthly_withdrawal_deposit['month'], avg_monthly_withdrawal_deposit['withdrawal'], marker='o', linestyle='-', label='Withdrawal')

plt.plot(avg_monthly_withdrawal_deposit['month'], avg_monthly_withdrawal_deposit['deposit'], marker='o', linestyle='-', label='Deposit')

plt.xlabel('Month')
plt.ylabel('Average Amount')
plt.title('Average Withdrawal and Deposit Amounts per Month')

plt.grid(True) 

plt.legend()
plt.savefig('result.jpg')
plt.show()
