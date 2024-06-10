import pandas as pd
import matplotlib.pyplot as plt

# Define the column names based on the observation
column_names = ['Date', 'Category', 'RefNo', 'ExtraDate', 'Withdrawal', 'Deposit', 'Balance']

# Load the dataset, skipping the first row and setting the column names
df = pd.read_csv('/workspace/MyTransaction.csv', skiprows=1, names=column_names)

# Custom function to parse dates with different year formats
def parse_date(date_str):
    if pd.isnull(date_str):
        return None
    if len(date_str.split('/')[-1]) == 2:
        return pd.to_datetime(date_str, format='%d/%m/%y')
    else:
        return pd.to_datetime(date_str, format='%d/%m/%Y')

# Apply the custom parse function to the 'Date' column
df['Date'] = df['Date'].apply(parse_date)

# Drop rows with NaN values in 'Date' column
df = df.dropna(subset=['Date'])

# Extract the month from the 'Date' column
df['Month'] = df['Date'].dt.strftime('%Y-%m')

# Group by month and calculate the average withdrawal and deposit amounts
monthly_averages = df.groupby('Month').agg({
    'Withdrawal': 'mean',
    'Deposit': 'mean'
}).reset_index()

# Plotting the line plot
plt.figure(figsize=(10, 5))
plt.plot(monthly_averages['Month'], monthly_averages['Withdrawal'], label='Withdrawal', marker='o')
plt.plot(monthly_averages['Month'], monthly_averages['Deposit'], label='Deposit', marker='o')
plt.title('Average Withdrawal and Deposit Amounts per Month')
plt.xlabel('Month')
plt.ylabel('Average Amount')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/workspace/result.jpg')
plt.close()
