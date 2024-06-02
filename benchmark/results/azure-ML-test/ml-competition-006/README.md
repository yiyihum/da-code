## Overview

**Welcome to the 2023 Kaggle Playground Series!** Thank you to everyone who participated in and contributed to Season 3 Playground Series so far!** **

**Your Goal:** For this Episode of the Series, your task is to use regression to predict the quality of wine based on various properties. Good luck!

Start

Jan 31, 2023

###### Close

Feb 14, 2023

### Evaluation

Submissions are scored based on the quadratic weighted kappa, which measures the agreement between two outcomes. This metric typically varies from 0 (random agreement) to 1 (complete agreement). In the event that there is less agreement than expected by chance, the metric may go below 0.

The quadratic weighted kappa is calculated as follows. First, an N x N histogram matrix** ***O* is constructed, such that** ***O~i,j~* corresponds to the number of** **`Id`s** ***i* (actual) that received a predicted value** ** *j* . An** ***N-by-N** ***matrix of weights,** ** *w* , is calculated based on the difference between actual and predicted values:

**𝑤**𝑖**,**𝑗**=**(**𝑖**−**𝑗**)**2**(**𝑁**−**1**)**2**

An** ***N-by-N* histogram matrix of expected outcomes,** ** *E* , is calculated assuming that there is no correlation between values.  This is calculated as the outer product between the actual histogram vector of outcomes and the predicted histogram vector, normalized such that** ***E* and** ***O* have the same sum.

From these three matrices, the quadratic weighted kappa is calculated as:

**𝜅**=**1**−**∑**𝑖**,**𝑗**𝑤**𝑖**,**𝑗**𝑂**𝑖**,**𝑗**∑**𝑖**,**𝑗**𝑤**𝑖**,**𝑗**𝐸**𝑖**,**𝑗**.**

## Submission File

For each** **`Id` in the test set, you must predict the value for the target** **`quality`. The file should contain a header and have the following format:

```
Id,quality
2056,5
2057,7
2058,3
etc.
```

# Wine Quality Dataset


## About Dataset

### Description:

This datasets is related to red variants of the Portuguese "Vinho Verde" wine.The dataset describes the amount of various chemicals present in wine and their effect on it's quality. The datasets can be viewed as classification or regression tasks. The classes are ordered and not balanced (e.g. there are much more normal wines than excellent or poor ones).Your task is to predict the quality of wine using the given data.

A simple yet challenging project, to anticipate the quality of wine.
The complexity arises due to the fact that the dataset has fewer samples, & is highly imbalanced.
Can you overcome these obstacles & build a good predictive model to classify them?

**This data frame contains the following columns:**

Input variables (based on physicochemical tests):
1 - fixed acidity
2 - volatile acidity
3 - citric acid
4 - residual sugar
5 - chlorides
6 - free sulfur dioxide
7 - total sulfur dioxide
8 - density
9 - pH
10 - sulphates
11 - alcohol
Output variable (based on sensory data):
12 - quality (score between 0 and 10)

### Acknowledgements:

This dataset is also available from Kaggle & UCI machine learning repository,** **[https://archive.ics.uci.edu/ml/datasets/wine+quality](https://archive.ics.uci.edu/ml/datasets/wine+quality).

### Objective:

* Understand the Dataset & cleanup (if required).
* Build classification models to predict the wine quality.
* Also fine-tune the hyperparameters & compare the evaluation metrics of various classification algorithms.
