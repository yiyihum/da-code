import pandas as pd
# Read datasets/monthly_deaths.csv into monthly
salaries = pd.read_csv("./ds_salaries_clean.csv")

# Find the 25th percentile
twenty_fifth = salaries["Salary_USD"].quantile(0.25)

# Save the median
salaries_median = salaries["Salary_USD"].median()

# Gather the 75th percentile
seventy_fifth = salaries["Salary_USD"].quantile(0.75)

# Create salary labels
salary_labels = ["entry", "mid", "senior", "exec"]

# Create the salary ranges list
salary_ranges = [0, twenty_fifth, salaries_median, seventy_fifth, salaries["Salary_USD"].max()]

# Create salary_level
salaries["salary_level"] = pd.cut(salaries["Salary_USD"],
                                  bins=salary_ranges,
                                  labels=salary_labels)

company_size_with_top_exec_level=salaries[salaries["salary_level"]=="exec"]['Company_Size'].value_counts().idxmax()
top10=salaries[salaries["Company_Size"]==company_size_with_top_exec_level].nlargest(10, 'Salary_USD')[['Designation', 'Salary_USD']]
top10.to_csv('./result.csv', index=False)