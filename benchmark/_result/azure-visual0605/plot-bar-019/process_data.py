import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset
df = pd.read_csv('/workspace/amazon.csv')

# Manually split the 'category' column into a list of subcategories
subcategories_list = df['category'].str.split('|').tolist()

# Flatten the list of lists into a single list of subcategories
flat_subcategories_list = [subcategory for sublist in subcategories_list for subcategory in sublist]

# Create a new DataFrame from the list of subcategories
subcategories_df = pd.DataFrame({'subcategories': flat_subcategories_list})

# Perform string replacements as per guidance.txt
replacements = {
    'HomeAppliances': 'Home Appliances',
    'AirQuality': 'Air Quality',
    'WearableTechnology': 'Wearable Technology',
    'NetworkingDevices': 'Networking Devices',
    'OfficePaperProducts': 'Office Paper Products',
    'ExternalDevices': 'External Devices',
    'DataStorage': 'Data Storage',
    'HomeStorage': 'Home Storage',
    'HomeAudio': 'Home Audio',
    'GeneralPurposeBatteries': 'General Purpose Batteries',
    'BatteryChargers': 'Battery Chargers',
    'CraftMaterials': 'Craft Materials',
    'OfficeElectronics': 'Office Electronics',
    'PowerAccessories': 'Power Accessories',
    'CarAccessories': 'Car Accessories',
    'HomeMedicalSupplies': 'Home Medical Supplies',
    'HomeTheater': 'Home Theater'
}

for original, replacement in replacements.items():
    subcategories_df['subcategories'] = subcategories_df['subcategories'].str.replace(original, replacement, regex=False)

# Count the occurrence of each subcategory
subcategory_counts = subcategories_df['subcategories'].value_counts().head(10)

# Create a bar chart
plt.figure(figsize=(16, 6))
subcategory_counts.plot(kind='barh', title='Most Amount of Products by Category')
plt.xlabel('Count')
plt.ylabel('Product Sub-Category')
plt.tight_layout()

# Save the bar chart as result.png
plt.savefig('/workspace/result.png')
