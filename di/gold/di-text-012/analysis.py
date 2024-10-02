#Importing Packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Importing Files
df = pd.read_csv('../amazon.csv')

# Checking Column Names
df.columns
# Checking Number of Rows and Columns
df.shape
# Checking Data Types for each Column
df.dtypes
# Changing the data type of discounted price and actual price
df['discounted_price'] = df['discounted_price'].str.replace("₹",'')
df['discounted_price'] = df['discounted_price'].str.replace(",",'')
df['discounted_price'] = df['discounted_price'].astype('float64')
df['actual_price'] = df['actual_price'].str.replace("₹",'')
df['actual_price'] = df['actual_price'].str.replace(",",'')
df['actual_price'] = df['actual_price'].astype('float64')
# Changing Datatype and values in Discount Percentage
df['discount_percentage'] = df['discount_percentage'].str.replace('%','').astype('float64')
df['discount_percentage'] = df['discount_percentage'] / 100
df['discount_percentage']
# Finding unusual string in the rating column
df['rating'].value_counts()
# Inspecting the strange row
df.query('rating == "|"')
# Changing Rating Columns Data Type
df['rating'] = df['rating'].str.replace('|', '4.0').astype('float64')
# Changing Rating Column Data Type
df['rating_count'] = df['rating_count'].str.replace(',', '').astype('float64')
# Checking for Duplicates
duplicates = df.duplicated()
df[duplicates]
# Checking Missing Values
df.isna().sum()
# Creating a new DataFrame with Selected Column
df1 = df[['product_id', 'product_name', 'category', 'discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count']].copy()
# Splitting the Strings in the category column
catsplit = df['category'].str.split('|', expand=True)
catsplit
# Renaming category column
catsplit = catsplit.rename(columns={0:'category_1', 1:'category_2', 2:'category_3'})
# Adding categories to the new dataframe
df1['category_1'] = catsplit['category_1']
df1['category_2'] = catsplit['category_2']
df1.drop(columns='category', inplace=True)

# Checking category_1 unique values
df1['category_1'].value_counts()
# Fixing Strings in the Category_1 Column
df1['category_1'] = df1['category_1'].str.replace('&', ' & ')
df1['category_1'] = df1['category_1'].str.replace('OfficeProducts', 'Office Products')
df1['category_1'] = df1['category_1'].str.replace('MusicalInstruments', 'Musical Instruments')
df1['category_1'] = df1['category_1'].str.replace('HomeImprovement', 'Home Improvement')
# Checking category_2 unique values
df1['category_2'].value_counts()
# Fixing Strings in Category_2 column
df1['category_2'] = df1['category_2'].str.replace('&', ' & ')
df1['category_2'] = df1['category_2'].str.replace(',', ', ')
df1['category_2'] = df1['category_2'].str.replace('HomeAppliances', 'Home Appliances')
df1['category_2'] = df1['category_2'].str.replace('AirQuality', 'Air Quality')
df1['category_2'] = df1['category_2'].str.replace('WearableTechnology', 'Wearable Technology')
df1['category_2'] = df1['category_2'].str.replace('NetworkingDevices', 'Networking Devices')
df1['category_2'] = df1['category_2'].str.replace('OfficePaperProducts', 'Office Paper Products')
df1['category_2'] = df1['category_2'].str.replace('ExternalDevices', 'External Devices')
df1['category_2'] = df1['category_2'].str.replace('DataStorage', 'Data Storage')
df1['category_2'] = df1['category_2'].str.replace('HomeStorage', 'Home Storage')
df1['category_2'] = df1['category_2'].str.replace('HomeAudio', 'Home Audio')
df1['category_2'] = df1['category_2'].str.replace('GeneralPurposeBatteries', 'General Purpose Batteries')
df1['category_2'] = df1['category_2'].str.replace('BatteryChargers', 'Battery Chargers')
df1['category_2'] = df1['category_2'].str.replace('CraftMaterials', 'Craft Materials')
df1['category_2'] = df1['category_2'].str.replace('OfficeElectronics', 'Office Electronics')
df1['category_2'] = df1['category_2'].str.replace('PowerAccessories', 'Power Accessories')
df1['category_2'] = df1['category_2'].str.replace('CarAccessories', 'Car Accessories')
df1['category_2'] = df1['category_2'].str.replace('HomeMedicalSupplies', 'Home Medical Supplies')
df1['category_2'] = df1['category_2'].str.replace('HomeTheater', 'Home Theater')
df1['product_id'].str.strip()
# Creating Categories for Rankings
rating_score = []
for score in df1['rating']:
    if score < 2.0 : rating_score.append('Poor')
    elif score < 3.0 : rating_score.append('Below Average')
    elif score < 4.0 : rating_score.append('Average')
    elif score < 5.0 : rating_score.append('Above Average')
    elif score == 5.0 : rating_score.append('Excellent')
# Creating A new Column and Changing the Data Type
df1['rating_score'] = rating_score
df1['rating_score'] = df1['rating_score'].astype('category')
# Reordered Categories
df1['rating_score'] = df1['rating_score'].cat.reorder_categories(['Below Average', 'Average', 'Above Average', 'Excellent'], ordered=True)
# Creating Difference of Price Column between Actual Price and Discounted Price
df1['difference_price'] = df1['actual_price'] - df1['discounted_price']
# Result After Cleaning and Preperation after first cleaned dataframe
df1.head()
# Subsetting Reviewers Identifications
reviewers = df[['user_id','user_name']]
# Splitting the strings in user_id column
reviewer_id_split = reviewers['user_id'].str.split(',', expand=False)
# Making user id display 1 id per row
reviewer_id_exp = reviewer_id_split.explode()
reviewer_id_clean = reviewer_id_exp.reset_index(drop=True)
#Splitting the strings in user_name column
reviewer_name_split = reviewers['user_name'].str.split(',', expand=False)
# Making user name display 1 id per row
review_name_exp = reviewer_name_split.explode()
reviewer_name_clean = review_name_exp.reset_index(drop=True)

# Creating 2 Data Frames to be merged
df21 = pd.DataFrame(data=reviewer_id_clean)
df22 = pd.DataFrame(data=reviewer_name_clean)
# Merging the 2 dataframe containing user_id and user_name
df2 = pd.merge(df21, df22, left_index=True, right_index=True)
# Main Category and Sub-Category
main_sub = df1[['category_1', 'category_2', 'product_id']]
main_sub = main_sub.rename(columns={'category_1' :'Main Category', 'category_2' : 'Sub-Category', 'product_id':'Product ID'})
main_sub_piv = pd.pivot_table(main_sub, index=['Main Category', 'Sub-Category'], aggfunc='count')
#Most amount of products by category

most_main_items = df1['category_1'].value_counts().head(5).rename_axis('category_1').reset_index(name='counts')

most_sub_items = df1['category_2'].value_counts().head(10).rename_axis('category_2').reset_index(name='counts')

fig, ax = plt.subplots(2, 1, figsize=(8, 10))
fig.suptitle('Most Amount of Products by Category', fontweight='heavy', size='x-large')

sns.barplot(ax=ax[0], data=most_main_items, x='counts', y='category_1')
sns.barplot(ax=ax[1], data=most_sub_items, x='counts', y='category_2')

plt.subplots_adjust(hspace = 0.3)

ax[0].set_xlabel('Count', fontweight='bold')
ax[0].set_ylabel('Product Main Category', fontweight='bold')

ax[1].set_xlabel('Count', fontweight='bold')
ax[1].set_ylabel('Product Sub-Category', fontweight='bold')

ax[0].set_title('Most Products by Main Category', fontweight='bold')
ax[1].set_title('Most Products by Sub-Category', fontweight='bold')


ax[0].bar_label(ax[0].containers[0])
ax[1].bar_label(ax[1].containers[0])

plt.show()

