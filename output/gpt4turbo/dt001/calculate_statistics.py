import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('/workspace/parts.csv')

# Define the rolling window size
window_size = 5

# Calculate rolling mean and standard deviation for the height measurements
data['rolling_mean'] = data['height'].rolling(window=window_size).mean()
data['rolling_std'] = data['height'].rolling(window=window_size).std()

# Establish control limits
data['upper_control_limit'] = data['rolling_mean'] + 3 * data['rolling_std']
data['lower_control_limit'] = data['rolling_mean'] - 3 * data['rolling_std']

# Flag measurements that fall outside the control limits
data['out_of_control'] = (data['height'] > data['upper_control_limit']) | (data['height'] < data['lower_control_limit'])

# Save the result to a CSV file
data.to_csv('/workspace/result.csv', index=False)
