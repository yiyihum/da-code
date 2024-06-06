import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

upi = pd.read_csv("../MyTransaction.csv")
upi_dup = upi.copy()
#handling the unnecessary Columns of Date and RefNo
upi_dup = upi_dup[['Date', 'Category', 'Withdrawal', 'Deposit', 'Balance']]
#Handiling the first row full of NaNs
upi_dup = upi_dup[1:]

transaction_counts = upi_dup['Category'].value_counts()
top_4_transaction = transaction_counts.head(4)
plt.figure(figsize=(8, 6))
plt.pie(top_4_transaction, labels=top_4_transaction.index, autopct="%1.1f%%")
plt.title("Transaction Distribution by Category")
plt.legend(bbox_to_anchor=(1.01, 1))
plt.savefig('result.jpg')
plt.show()