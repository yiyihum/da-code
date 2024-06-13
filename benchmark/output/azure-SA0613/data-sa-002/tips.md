**Data Grouping:**

The data is divided into groups (holidays and working days) and stored in `grpA` and `grpB` respectively.

**Normality Test:**

The Shapiro-Wilk test is used to check the normality of both groups. The test returns a t-statistic and p-value. A p-value less than 0.05 indicates that the data does not follow a normal distribution.
`ntA` and `ntB` indicate whether group A and group B follow a normal distribution, respectively.

**Homogeneity of Variances Test (Parametric Test):**

If the data of both groups are normally distributed, the Levene test is performed to check if the variances of the two groups are equal.
Based on the result of the Levene test, the appropriate t-test is chosen: a standard t-test if the variances are equal, or Welch's t-test if the variances are unequal.

**Non-Parametric Test:**

If either group does not follow a normal distribution, the Mann-Whitney U test is used. This is a non-parametric test.

**Result Generation:**

A dataframe containing the test results is generated, including whether to reject the null hypothesis, the p-value, the type of test (parametric or non-parametric), and comments.


If the p-value > 0.05, fail to reject the null hypothesis; if the p-value < 0.05, reject the null hypothesis.
The results should be filled in the corresponding `ab_test_results.csv` file.

CSV output requirements:
- **test_type**: The type of statistical test used, classified into "Parametric" and "Non Parametric".
- **AB Hypothesis**: Whether to reject the null hypothesis, with values "Strong Evidence To Reject NULL Hypothesis" or "No Evidence To Reject NULL Hypothesis".
- **P-Value**: The p-value of the test result.
- **Comment**: Comments on the results, with values "A/B Groups Are Similar" or "A/B Groups Are Not Similar".
