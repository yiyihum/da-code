# Binary Classification with a Bank Churn Dataset

## Overview

**Welcome to the 2024 Kaggle Playground Series!** Happy New Year! This is the 1st episode of Season 4. We plan to continue in the spirit of previous playgrounds, providing interesting an approachable datasets for our community to practice their machine learning skills, and anticipate a competition each month.** **

**Your Goal:** For this Episode of the Series, your task is to predict whether a customer continues with their account or closes it (e.g., churns). Good luck!

### Evaluation

Submissions are evaluated on area under the ROC curve between the predicted probability and the observed target.

## Submission File

For each** **`id` in the test set, you must predict the probability for the target variable** **`Exited`. The file should contain a header and have the following format:

```
id,Exited
165034,0.9
165035,0.1
165036,0.5
etc.
```

# Bank Customer Churn Prediction

## About Dataset

The bank customer churn dataset is a commonly used dataset for predicting customer churn in the banking industry. It contains information on bank customers who either left the bank or continue to be a customer. The dataset includes the following attributes:

1. Customer ID: A unique identifier for each customer
2. Surname: The customer's surname or last name
3. Credit Score: A numerical value representing the customer's credit score
4. Geography: The country where the customer resides (France, Spain or Germany)
5. Gender: The customer's gender (Male or Female)
6. Age: The customer's age.
7. Tenure: The number of years the customer has been with the bank
8. Balance: The customer's account balance
9. NumOfProducts: The number of bank products the customer uses (e.g., savings account, credit card)
10. HasCrCard: Whether the customer has a credit card (1 = yes, 0 = no)
11. IsActiveMember: Whether the customer is an active member (1 = yes, 0 = no)
12. EstimatedSalary: The estimated salary of the customer
13. Exited: Whether the customer has churned (1 = yes, 0 = no)
