import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 

plt.style.use('ggplot')
pd.set_option('display.max_columns',24)
pd.set_option('display.max_colwidth',None)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

data=pd.read_excel('../Superstore.xlsx',sheet_name='Orders')
data.head(3)
data.info()

data=data.drop('Row ID',axis=1)

data=data[[ 
        'Order ID', 
        'Order Date', 
        'Ship Date', 
        'Ship Mode', 
    #'Customer ID',
    #'Customer Name', 
        'Segment', 
    #'Country', 
        'City', 
        'State', 
    #'Postal Code',
        'Region', 
    #'Product ID', 
        'Category', 
        'Sub-Category', 
        'Product Name',
        'Sales', 
        'Quantity', 
        'Discount', 
        'Profit']]
data.head(3) # final dataframe, after columns were removed

# feature engineering, extracts specific date values from the `Order Date` column, creates new features from existing features
data['month']=data['Order Date'].dt.month 
data['year']=data['Order Date'].dt.year
data['year_month']=data['Order Date'].dt.to_period('M')
data['total_discount_in_dollars']=data['Sales'] * data['Discount'] # discount's equivalent to dollars
data['selling_price']=data['Sales'] / data['Quantity'] # calculates selling price for the each product
data['(net)_profit_before_discount']=data['Sales'] * data['Discount'] + data['Profit'] # net profit before deducting discount
data['order_fulfillment_time']=data['Ship Date'] - data['Order Date'] # interval between order placed and order shipped
data['net_profit_per_unit_sold']=data['Profit'] / data['Quantity'] # net profit generated per unit sold
data=data.rename(columns={'Profit':'net_profit'}) # renames Profit column with net_profit, a more specific name
data['profit_margin']=data['net_profit'] / data['Sales'] * 100 # for a 25% profit margin, the company makes .25 dollars per 1 dollar sale
data['discounted_sales']=data['Sales'] - (data['Discount']*data['Sales']) # extracts sales accounted for discount

print('Output dataframe:')
data.head(5)

data.groupby('year_month')['Sales'].sum().plot(c='#003f5c',linewidth=1,figsize=(12,6))
plt.title('Total Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Total Sales')

plt.tight_layout()
plt.savefig("result.png")
