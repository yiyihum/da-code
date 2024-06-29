import pandas as pd
import re

# Load the dataset
df = pd.read_csv('/workspace/parking_violation.csv')

# Define cleaning functions
def normalize_vehicle_color(color):
    if pd.isnull(color):
        return color
    color = str(color).upper()
    if color in ['GREY', 'GRAY']:
        return 'GRAY'
    return color

def convert_to_boolean(value):
    if pd.isnull(value):
        return value
    value = str(value).strip().upper()
    if value in ['YES', 'Y']:
        return 'Yes'
    elif value in ['NO', 'N']:
        return 'No'
    else:
        return None

# Apply cleaning functions to the dataframe
df['Vehicle Color'] = df['Vehicle Color'].apply(normalize_vehicle_color)
df['Unregistered Vehicle?'] = df['Unregistered Vehicle?'].apply(convert_to_boolean)
df['No Standing or Stopping Violation'] = df['No Standing or Stopping Violation'].apply(convert_to_boolean)
df['Hydrant Violation'] = df['Hydrant Violation'].apply(convert_to_boolean)
df['Double Parking Violation'] = df['Double Parking Violation'].apply(convert_to_boolean)

# Save the cleaned dataframe to a new CSV file
cleaned_file_path = '/workspace/cleaned_parking_violation.csv'
df.to_csv(cleaned_file_path, index=False)

print(f"Data cleaned and saved to {cleaned_file_path}")
