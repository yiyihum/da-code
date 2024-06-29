## Overview

### Description

### Goal of the Competition

The goal of this competition is to predict if a person has any of three medical conditions. You are being asked to predict if the person has one or more of any of the three medical conditions (Class 1), or none of the three medical conditions (Class 0). You will create a model trained on measurements of health characteristics.

To determine if someone has these medical conditions requires a long and intrusive process to collect information from patients. With predictive models, we can shorten this process and keep patient details private by collecting key characteristics relative to the conditions, then encoding these characteristics.

Your work will help researchers discover the relationship between measurements of certain characteristics and potential patient conditions.

## Context

They say age is just a number but a whole host of health issues come with aging. From heart disease and dementia to hearing loss and arthritis, aging is a risk factor for numerous diseases and complications. The growing field of bioinformatics includes research into interventions that can help slow and reverse biological aging and prevent major age-related ailments. Data science could have a role to play in developing new methods to solve problems with diverse data, even if the number of samples is small.

Currently, models like XGBoost and random forest are used to predict medical conditions yet the models' performance is not good enough. Dealing with critical problems where lives are on the line, models need to make correct predictions reliably and consistently between different cases.

Founded in 2015, competition host** **[InVitro Cell Research, LLC (ICR)](https://invitrocellresearch.com/) is a privately funded company focused on regenerative and preventive personalized medicine. Their offices and labs in the greater New York City area offer state-of-the-art research space. InVitro Cell Research's Scientists are what set them apart, helping guide and defining their mission of researching how to repair aging people fast.

In this competition, you’ll work with measurements of health characteristic data to solve critical problems in bioinformatics. Based on minimal training, you’ll create a model to predict if a person has any of three medical conditions, with an aim to improve on existing methods.

You could help advance the growing field of bioinformatics and explore new methods to solve complex problems with diverse data.

> **This is a Code Competition. Refer to** **[Code Requirements](https://kaggle.com/competitions/icr-identify-age-related-conditions/overview/code-requirements) for details.**

### Evaluation

link

keyboard_arrow_up

Submissions are evaluated using a** ** **balanced logarithmic loss** . The overall effect is such that each class is roughly equally important for the final score.

Each observation is either of class** **`0` or of class** **`1`. For each observation, you must submit a probability for each class. The formula is then:

**Log Loss**=**−**1**𝑁**0**∑**𝑁**0**𝑖**=**1**𝑦**0**𝑖**log**𝑝**0**𝑖**−**1**𝑁**1**∑**𝑁**1**𝑖**=**1**𝑦**1**𝑖**log**𝑝**1**𝑖**2**

where (N_{c}) is the number of observations of class (c), (\log) is the natural logarithm, (y_{c i}) is 1 if observation (i) belongs to class (c) and 0 otherwise, (p_{c i}) is the predicted probability that observation (i) belongs to class (c).

The submitted probabilities for a given row are not required to sum to one because they are rescaled prior to being scored (each row is divided by the row sum). In order to avoid the extremes of the log function, each predicted probability** **𝑝** **is replaced with** **max**(**min**(**𝑝**,**1**−**10**−**15**)**,**10**−**15**).

## Submission File

For each** **`id` in the test set, you must predict a probability for each of the two classes. The file should contain a header and have the following format:

```
Id,class_0,class_1
00eed32682bb,0.5,0.5
010ebe33f668,0.5,0.5
02fa521e1838,0.5,0.5
040e15f562a2,0.5,0.5
046e85c7cc7f,0.5,0.5
...
```
