import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

upi = pd.read_csv("../MyTransaction.csv")

transaction_counts = upi['Category'].value_counts()
top_4_transaction = transaction_counts.head(4)
plt.figure(figsize=(8, 6))
plt.pie(top_4_transaction, labels=top_4_transaction.index, autopct="%1.1f%%")
plt.title("Transaction Distribution by Category")
plt.savefig('answer1.png')


# month_counts = upi_dup['Month'].value_counts().sort_index()
# plt.figure(figsize=(8, 6))
# plt.bar(month_counts.index, month_counts.values)  
# plt.title('Monthly Transactions') 
# plt.xticks(range(1, 13))  
# plt.savefig('answer2.png') 
