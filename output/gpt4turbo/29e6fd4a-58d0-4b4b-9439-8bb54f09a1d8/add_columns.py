import pandas as pd

# Load the existing CSV file
df = pd.read_csv('/workspace/cars_details_merges.csv')

# Define the new columns with their default values and data types based on the schema
new_columns = {
    "loc": str, "myear": int, "bt": str, "tt": str, "ft": str, "km": int, "ip": int,
    "images": object, "imgCount": int, "threesixty": bool, "dvn": str, "oem": str,
    "model": str, "variantName": str, "city_x": str, "pu": int, "discountValue": int,
    "utype": str, "carType": str, "top_features": object, "comfort_features": object,
    "interior_features": object, "exterior_features": object, "safety_features": object,
    "Color": str, "Engine Type": str, "Max Power": str, "Max Torque": str,
    "No of Cylinder": int, "Length": int, "Width": int, "Height": int
}

# Add the new columns to the DataFrame with default values
for column, dtype in new_columns.items():
    if dtype == bool:
        df[column] = False  # Use False as the default for boolean columns
    else:
        df[column] = None  # Use None (NaN) for other types as default

# Save the updated DataFrame to a new CSV file
df.to_csv('/workspace/cars_details_merges.csv', index=False)
