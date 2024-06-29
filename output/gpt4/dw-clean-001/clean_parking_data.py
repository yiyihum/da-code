import pandas as pd
import re

# Load the dataset
df = pd.read_csv('/workspace/parking_violation.csv')

# Define cleaning functions
def clean_summons_number(number):
    return str(number).zfill(4) if pd.notnull(number) else number

def clean_plate_id(plate_id):
    return plate_id if re.match(r'.*?\d{4}$', str(plate_id)) else None

def clean_registration_state(state):
    return state if len(state) == 2 and state.isalpha() else None

def clean_plate_type(plate_type):
    return plate_type if plate_type in ['PAS', 'SAF'] else None

def clean_issue_date(date):
    return pd.to_datetime(date, format='%m/%d/%Y', errors='coerce')

def clean_violation_code(code):
    return code if re.match(r'^[1-9][0-9]$', str(code)) else None

def clean_vehicle_body_type(body_type):
    return 'TRK' if body_type == 'P-U' else ('Unknown' if pd.isnull(body_type) else body_type)

def clean_vehicle_make(make):
    return make if re.match(r'^[A-Z]$', str(make)) else None

def clean_street_code(code):
    return code if re.match(r'\d{5}', str(code)) else None

def clean_vehicle_expiration_date(date):
    return pd.to_datetime(date, format='%m/%d/%Y', errors='coerce')

def clean_violation_location(location):
    return location if re.match(r'\d+', str(location)) else None

def clean_violation_precinct(precinct):
    return precinct if re.match(r'\d+', str(precinct)) else None

# Apply cleaning functions to the dataframe
df['Summons Number'] = df['Summons Number'].apply(clean_summons_number)
df['Plate ID'] = df['Plate ID'].apply(clean_plate_id)
df['Registration State'] = df['Registration State'].apply(clean_registration_state)
df['Plate Type'] = df['Plate Type'].apply(clean_plate_type)
df['Issue Date'] = df['Issue Date'].apply(clean_issue_date)
df['Violation Code'] = df['Violation Code'].apply(clean_violation_code)
df['Vehicle Body Type'] = df['Vehicle Body Type'].apply(clean_vehicle_body_type)
df['Vehicle Make'] = df['Vehicle Make'].apply(clean_vehicle_make)
df['Street Code1'] = df['Street Code1'].apply(clean_street_code)
df['Street Code2'] = df['Street Code2'].apply(clean_street_code)
df['Street Code3'] = df['Street Code3'].apply(clean_street_code)
df['Vehicle Expiration Date'] = df['Vehicle Expiration Date'].apply(clean_vehicle_expiration_date)
df['Violation Location'] = df['Violation Location'].apply(clean_violation_location)
df['Violation Precinct'] = df['Violation Precinct'].apply(clean_violation_precinct)

# Save the cleaned dataframe to a new CSV file
cleaned_file_path = '/workspace/cleaned_parking_violation.csv'
df.to_csv(cleaned_file_path, index=False)

print(f"Data cleaned and saved to {cleaned_file_path}")
