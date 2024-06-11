import datetime as dt
import pandas as pd

online = pd.read_csv('DC3-1_0\\online.csv')
# Define a function that will parse the date
def get_day(date_str):
    # 首先使用strptime将字符串解析成datetime对象
    date_dt = dt.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    
    # 然后提取出日期部分
    return dt.datetime(date_dt.year, date_dt.month, date_dt.day)

def get_date_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    day = df[column].dt.day
    return year, month, day

# Create InvoiceDay column
online['InvoiceDay'] = online['InvoiceDate'].apply(get_day) 

# Group by CustomerID and select the InvoiceDay value
grouping = online.groupby('CustomerID')['InvoiceDay'] 

# Assign a minimum InvoiceDay value to the dataset
online['CohortDay'] = grouping.transform('min')

# Get the integers for date parts from the InvoiceDaycolumn
invoice_year, invoice_month, invoice_day = get_date_int(online, 'InvoiceDay')

# Get the integers for date parts from the CohortDay column
cohort_year, cohort_month, cohort_day = get_date_int(online, 'CohortDay')

# Calculate difference in years
years_diff = invoice_year - cohort_year

# Calculate difference in months
months_diff = invoice_month - cohort_month

# Calculate difference in days
days_diff = invoice_day - cohort_day

# Extract the difference in days from all previous values
online['CohortIndex'] = years_diff * 365 + months_diff * 30 + days_diff + 1

df_selected = online[['InvoiceNo', 'CohortIndex']]

# 将结果保存到新的CSV文件
df_selected.to_csv('result.csv', index=False)