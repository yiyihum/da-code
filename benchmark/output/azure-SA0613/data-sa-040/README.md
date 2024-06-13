# *Hypothesis Testing in Healthcare*

![Untitled](https://github.com/Khangtran94/Hypothesis_Testing_in_Healthcare/assets/146164801/defce619-cf43-42b2-ad4d-881fd61dc6ea)

## Target goal:

* Assess the significance of the drug's adverse reactions.

### Methods Used:
* Two samples proportions z-test.
* Chi-square test of independence.
* Mann-Whitney U test.

### Technologies:
* Python / Jupyter Notebook.
* Pandas, sklearn, matplotlib, numpy, pingouin, statsmodels.

# Dataset information:
* The dataset has **16103 rows** and **8 columns**.

![Untitled](https://github.com/Khangtran94/Hypothesis_Testing_in_Healthcare/assets/146164801/c8339030-28d7-4adf-8032-9f5c536704ec)

![Untitled](https://github.com/Khangtran94/Hypothesis_Testing_in_Healthcare/assets/146164801/9bf8aae0-618e-4625-8f64-20ce3b9dd733)

* The dataset provided contained five adverse effects: headache, abdominal pain, dyspepsia, upper respiratory infection, chronic obstructive airway disease (COAD), demographic data, vital signs, lab measures, etc.
* The ratio of drug observations to placebo observations is 2 to 1.

## Step by step:
### 1. Count the adverse_effects column values for each trx group:

![Untitled](https://github.com/Khangtran94/Hypothesis_Testing_in_Healthcare/assets/146164801/f372c2a2-b3f3-4dd0-a819-e86a5bd4a39a)

### 2. Compute total rows in each group:

![Untitled](https://github.com/Khangtran94/Hypothesis_Testing_in_Healthcare/assets/146164801/91119ed0-2761-4336-bdac-e98f15fffbb3)

### 3. Proportions Z-Test:
* Null Hypothesis: The proportion of adverse effects is the same in the Drug and Placebo groups.
* Alternative Hypothesis: The proportion of adverse effects is different between the Drug and Placebo groups.

![image](https://github.com/Khangtran94/Hypothesis_Testing_in_Healthcare/assets/146164801/681d24c5-acf5-4fa9-9bef-8214239bc996)

* Conclusion: Based on the results, there is not enough evidence to reject the null hypothesis. The proportions of adverse effects in the two groups are not significantly different, and any observed difference is likely due to random variability.

### 4. Chi-Squared Test:
* Null Hypothesis: The number of adverse effects is independent of the treatment and control groups.
* Alternative Hypothesis: There is a significant association between the number of adverse effects and the treatment groups.

![Untitled](https://github.com/Khangtran94/Hypothesis_Testing_in_Healthcare/assets/146164801/149f0f68-871f-44f6-97df-27df82f009aa)

* Conclusion: With a p-value of 0.6150, we fail to reject the null hypothesis. There is insufficient evidence to conclude that the number of adverse effects is dependent on the treatment groups (Drug and Placebo). The observed association is not statistically significant.
  
### 5. Conducting a normality test: 
* To choose between unpaired t-test and Wilcoxon-Mann-Whitney test.

![Untitled](https://github.com/Khangtran94/Hypothesis_Testing_in_Healthcare/assets/146164801/c2e31cda-7b79-4d12-bb63-c09a7cc30bd9)

* The histograms being similar suggests that there is an overlap in the age ranges of individuals in the Drug and Placebo groups. This implies that individuals with similar ages are present in both treatment groups.
* The data distribution is not normal.
* Therefore, we will choose Mean Whitney U for further analysis.

### 6. Mann-Whitney U Test:

* Null Hypothesis: There is no significant difference in the distribution of ages between the Drug and Placebo groups.
* Alternative Hypothesis: There is a significant difference in the distribution of ages between the Drug and Placebo groups.

![Untitled](https://github.com/Khangtran94/Hypothesis_Testing_in_Healthcare/assets/146164801/08f0785f-46ec-4435-9327-579ce72ca4f9)

* Conclusion: The p-value (0.256963) is greater than a common significance level (e.g., 0.05). Therefore, based on this test, there is not enough evidence to reject the null hypothesis that there is no difference between the distributions of age_trx and age_placebo.

## **CONCLUSION:**
### Adverse Effects Proportions:
* The proportions Z-test suggests that the proportion of adverse effects is similar between the Drug and Placebo groups. The lack of statistical significance indicates that any observed differences are likely due to random variability.

### Number of Adverse Effects:
* The chi-squared test indicates that the number of adverse effects is not significantly associated with the treatment groups. There is no evidence to suggest that the treatment type influences the number of adverse effects.

### Age Distribution:
* The Mann-Whitney U test shows no significant difference in the distribution of ages between the Drug and Placebo groups. Age does not appear to be a differentiating factor between the two treatment groups.
