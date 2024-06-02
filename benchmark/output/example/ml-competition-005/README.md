## Overview

**Welcome to the 2023 Kaggle Playground Series!** Thank you to everyone who participated in and contributed to Season 3 Playground Series so far. This is our last episode for the Season 3 and we wish you all a Happy New Year! Stay tuned for the new season next year!

**Your Goal:** For this Episode of the Series, your task is to use a multi-class approach to predict the the outcomes of patients with cirrhosis. Good luck!

Start

Dec 5, 2023

###### Close

Jan 2, 2024

### Evaluation

link

keyboard_arrow_up

Submissions are evaluated using the multi-class logarithmic loss. Each** **`id` in the test set had a single true class label,** **`Status`. For each** **`id`, you must submit a set of predicted probabilities for each of the three possible outcomes, e.g.,** **`Status_C`,** **`Status_CL`, and** **`Status_D`.

The metric is calculated

**𝑙**𝑜**𝑔**𝑙**𝑜**𝑠**𝑠**=**−**1**𝑁**∑**𝑖**=**1**𝑁**∑**𝑗**=**1**𝑀**𝑦**𝑖**𝑗**log**(**𝑝**𝑖**𝑗**)**,**

where** **𝑁** **is the number of rows in the test set,** **𝑀** **is the number of outcomes (i.e., 3), ** **𝑙**𝑜**𝑔** **is the natural logarithm,** **𝑦**𝑖**𝑗** **is 1 if row** **𝑖** **has the ground truth label** **𝑗** **and 0 otherwise, and** **𝑝**𝑖**𝑗** **is the predicted probability that observation** **𝑖** **belongs to class **𝑗**.

The submitted probabilities for a given row are not required to sum to one because they are rescaled prior to being scored (each row is divided by the row sum). In order to avoid the extremes of the log function, predicted probabilities are replaced with** **𝑚**𝑎**𝑥**(**𝑚**𝑖**𝑛**(**𝑝**,**1**−**10**−**15**)**,**10**−**15**).

## Submission File

For each** **`id` row in the test set, you must predict probabilities of the three outcomes** **`Status_C`,** **`Status_CL`, and** **`Status_D` . The file should contain a header and have the following format:

```
id,Status_C,Status_CL,Status_D
7905,0.628084,0.034788,0.337128
7906,0.628084,0.034788,0.337128
7907,0.628084,0.034788,0.337128
etc.
```



# Cirrhosis Patient Survival Prediction


## About Dataset

Utilize 17 clinical features for predicting survival state of patients with liver cirrhosis. The survival states include 0 = D (death), 1 = C (censored), 2 = CL (censored due to liver transplantation).

**For what purpose was the dataset created?**

Cirrhosis results from prolonged liver damage, leading to extensive scarring, often due to conditions like hepatitis or chronic alcohol consumption. The data provided is sourced from a Mayo Clinic study on primary biliary cirrhosis (PBC) of the liver carried out from 1974 to 1984.

**Who funded the creation of the dataset?**

Mayo Clinic

**What do the instances in this dataset represent?**

People

**Does the dataset contain data that might be considered sensitive in any way?**

Gender, Age

**Was there any data preprocessing performed?**

1. Drop all the rows where miss value (NA) were present in the Drug column
2. Impute missing values with mean results
3. One-hot encoding for all category attributes

**Additional Information**

During 1974 to 1984, 424 PBC patients referred to the Mayo Clinic qualified for the randomized placebo-controlled trial testing the drug D-penicillamine. Of these, the initial 312 patients took part in the trial and have mostly comprehensive data. The remaining 112 patients didn't join the clinical trial but agreed to record basic metrics and undergo survival tracking. Six of these patients were soon untraceable after their diagnosis, leaving data for 106 of these individuals in addition to the 312 who were part of the randomized trial.
