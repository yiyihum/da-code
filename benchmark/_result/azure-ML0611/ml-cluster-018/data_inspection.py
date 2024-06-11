import pandas as pd

# Load the data
df = pd.read_excel('/workspace/Online Retail.xlsx')

# Check for missing values
missing_values = df.isnull().sum()

# Get summary statistics for numeric columns
summary_statistics = df.describe()

# Print the missing values and summary statistics
print("Missing Values:\n", missing_values)
print("\nSummary Statistics:\n", summary_statistics)
