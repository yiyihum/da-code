import pandas as pd

# Load the data
charging_sessions = pd.read_csv('charging_sessions.csv')

# Filter for shared users
shared_sessions = charging_sessions[charging_sessions['user_type'] == 'Shared']

# Group by weekdays and start hour, then count the number of sessions
grouped_sessions = shared_sessions.groupby(['weekdays_plugin', 'start_plugin_hour']).size().reset_index(name='session_count')

# Sort the results to get the ten busiest periods
top_ten_busy_periods = grouped_sessions.sort_values(by='session_count', ascending=False).head(10)

# Save the results to a CSV file
top_ten_busy_periods.to_csv('/workspace/top_ten_busy_periods.csv', index=False)
