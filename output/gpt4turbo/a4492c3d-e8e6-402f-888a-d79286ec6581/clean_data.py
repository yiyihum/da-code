import sqlite3
import re
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('/workspace/parking_violation.db')
cursor = conn.cursor()

# Function to convert date from MM/DD/YYYY to YYYY-MM-DD
def convert_date_format(date_str):
    try:
        if isinstance(date_str, int):
            # Convert integer to string assuming it's in the format YYYYMMDD
            date_str = str(date_str)
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return None

# Function to validate and clean data
def clean_data():
    # Fetch all records from the database
    cursor.execute("SELECT * FROM parking_violation")
    records = cursor.fetchall()

    # Prepare the update statement with correct column names
    update_stmt = """
    UPDATE parking_violation
    SET `Plate ID` = ?,
        `Registration State` = ?,
        `Plate Type` = ?,
        `Issue Date` = ?,
        `Violation Code` = ?,
        `Vehicle Body Type` = ?,
        `Vehicle Make` = ?,
        `Street Code1` = ?,
        `Street Code2` = ?,
        `Street Code3` = ?,
        `Vehicle Expiration Date` = ?,
        `Violation Location` = ?
    WHERE `Summons Number` = ?
    """

    # Iterate over each record and clean the data
    for record in records:
        # Access columns by index
        summons_number = record[0]
        plate_id = record[1]
        reg_state = record[2]
        plate_type = record[3]
        issue_date = record[4]
        violation_code = record[5]
        vehicle_body_type = record[6]
        vehicle_make = record[7]
        street_code1 = record[9]
        street_code2 = record[10]
        street_code3 = record[11]
        vehicle_expiration_date = record[12]
        violation_location = record[13]

        # Clean and validate data according to the standards
        plate_id = re.sub(r'---(\d{4})$', r'\1', plate_id) if re.match(r'---\d{4}$', plate_id) else plate_id
        issue_date = convert_date_format(issue_date) if issue_date and isinstance(issue_date, str) else None
        vehicle_body_type = 'TRK' if vehicle_body_type == 'P-U' else vehicle_body_type or 'Unknown'
        vehicle_make = vehicle_make if isinstance(vehicle_make, str) and re.match(r'^[A-Z]$', vehicle_make) else None
        street_code1 = f"{int(street_code1):05}" if isinstance(street_code1, int) else street_code1
        street_code2 = f"{int(street_code2):05}" if isinstance(street_code2, int) else street_code2
        street_code3 = f"{int(street_code3):05}" if isinstance(street_code3, int) else street_code3
        vehicle_expiration_date = convert_date_format(str(vehicle_expiration_date)) if vehicle_expiration_date else None
        violation_location = str(int(violation_location)) if isinstance(violation_location, float) else violation_location

        # Update the record in the database
        cursor.execute(update_stmt, (plate_id, reg_state, plate_type, issue_date, violation_code, vehicle_body_type, vehicle_make, street_code1, street_code2, street_code3, vehicle_expiration_date, violation_location, summons_number))

    # Commit the changes
    conn.commit()

# Run the clean_data function
clean_data()

# Close the database connection
conn.close()
