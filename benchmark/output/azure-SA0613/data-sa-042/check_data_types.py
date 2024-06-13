import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/Books_df.csv')

# Check the data types of the 'Price' and 'No. of People Rated' columns
price_dtype = df['Price'].dtype
ratings_dtype = df['No. of People Rated'].dtype

# Print the data types
print(f"Data type of 'Price': {price_dtype}")
print(f"Data type of 'No. of People Rated': {ratings_dtype}")
