import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../Building_Permits.csv')

date_columns = ['Permit Creation Date', 'Current Status Date', 'Filed Date', 'Issued Date',
                 'Completed Date', 'First Construction Document Date', 'Permit Expiration Date']
df[date_columns] = df[date_columns].astype('datetime64[ns]')

mean_days_permit_type = df.groupby('Permit Type Definition')['Days_to_Issue'].mean().reset_index()
mean_days_permit_type = mean_days_permit_type.sort_values(by='Days_to_Issue')

df['Days_to_Issue'] = (df['Issued Date'] - df['Filed Date']).dt.days
fire_only_permit_counts = df['Fire Only Permit'].value_counts()
structural_notification_counts = df['Structural Notification'].value_counts()
site_permit_counts = df['Site Permit'].value_counts()
df['Weekday'] = df['Filed Date'].dt.day_name()

average_days_per_weekday = df.groupby('Weekday')['Days_to_Issue'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.bar(average_days_per_weekday['Weekday'], average_days_per_weekday['Days_to_Issue'], color='skyblue')
plt.xlabel('Weekday')
plt.ylabel('Average Days to Issue')
plt.title('Average Days to Issue by Weekday')

plt.savefig('./result.png')