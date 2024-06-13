import pandas as pd

# Load the historical stock data
data = pd.read_csv('/workspace/GE - Historical.csv')

# Convert the Date column to datetime type
data['Date'] = pd.to_datetime(data['Date'])

# Calculate daily losses as the negative daily return
data['Daily Loss'] = -(data['Close'].pct_change())

# Filter the data for January 2010
january_2010_data = data[(data['Date'] >= '2010-01-01') & (data['Date'] < '2010-02-01')]

# Calculate weekly losses by resampling to weekly frequency and taking the sum
january_2010_data.set_index('Date', inplace=True)
weekly_losses = january_2010_data['Daily Loss'].resample('W').sum()

# Display the weekly losses
print(weekly_losses)
