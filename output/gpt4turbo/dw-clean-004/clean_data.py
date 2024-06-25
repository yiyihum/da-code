import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/data.csv')

# Replace '?' with NaN
df.replace('?', pd.NA, inplace=True)

# Convert columns to appropriate data types
numerical_columns = ['normalized-losses', 'bore', 'stroke', 'horsepower', 'peak-rpm']
df[numerical_columns] = df[numerical_columns].apply(pd.to_numeric, errors='coerce')

# Replace missing values in numerical columns with their respective means
for column in numerical_columns:
    df[column].fillna(df[column].mean(), inplace=True)

# Replace missing values in 'num-of-doors' with the most frequent value
most_frequent = df['num-of-doors'].mode()[0]
df['num-of-doors'].fillna(most_frequent, inplace=True)

# Delete rows with missing values in the 'price' column
df.dropna(subset=['price'], inplace=True)

# Convert 'price' to numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Save the cleaned data to a new CSV file
cleaned_data_path = '/workspace/cleaned_data.csv'
df.to_csv(cleaned_data_path, index=False)

# Display the number of missing values in each column after cleaning
print(df.isnull().sum())
