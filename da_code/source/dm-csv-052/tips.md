#### Definations

* snapshot date: 2011-12-10 00:00:00

* Recency (R): Measures how many days have passed since the customer's most recent transaction relative to the snapshot date.

* Frequency (F): Counts how many times a customer has made a purchase within the time frame being analyzed. This is often done by counting the number of invoices (as each invoice is typically associated with a purchase).

* Monetary Value (M): Reflects the total amount of money a customer has spent during the time frame being analyzed, which you obtain by summing up all of a customer's transactions.

#### Possible steps
Sort customers into groups based on how recently they bought something, how often they buy, and how much money they spend. Think of it like giving grades to customers to see who are the best and who might need more attention. Use 1~4 to present different groups.
1. You should group the customers into three separate groups based on Recency, and Frequency, assign these labels to four equal percentile groups.
2. Assign customers to four groups based on the MonetaryValue percentiles and then calculate an RFM_Score which is a sum of the R, F, and M values.
3. If the RFM score is greater than or equal to 10, the level should be "Top". If it's between 6 and 10 it should be "Middle", and otherwise it should be "Low".
