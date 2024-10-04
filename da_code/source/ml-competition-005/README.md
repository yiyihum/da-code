## Competition

Submissions are evaluated using the multi-class logarithmic loss. Each** **`id` in the test set had a single true class label,** **`Status`. For each** **`id`, you must submit a set of predicted probabilities for each of the three possible outcomes, e.g.,** **`Status_C`,** **`Status_CL`, and** **`Status_D`**.

The metric is calculated as logloss

The submitted probabilities for a given row are not required to sum to one because they are rescaled prior to being scored (each row is divided by the row sum). In order to avoid the extremes of the log function, predicted probabilities are replaced with** **𝑚**𝑎**𝑥**(**𝑚**𝑖**𝑛**(**𝑝**,**1e**−**15**), 1-**1e**−**15**).

## Submission File

For each  **`id` row in the test set, you must predict probabilities of the three outcomes** **`Status_C`,** **`Status_CL`, and** **`Status_D` . The file should contain a header and have the following format:

```
id,Status_C,Status_CL,Status_D
7905,0.628084,0.034788,0.337128
7906,0.628084,0.034788,0.337128
7907,0.628084,0.034788,0.337128
etc.
```

# Cirrhosis Patient Survival Prediction Dataset

## About Dataset

Utilize 17 clinical features for predicting survival state of patients with liver cirrhosis. The survival states include 0 = D (death), 1 = C (censored), 2 = CL (censored due to liver transplantation).
