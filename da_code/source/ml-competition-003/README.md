## Overview

### Description

### Goal of the Competition

The goal of this competition is to predict if a person has any of three medical conditions. You are being asked to predict if the person has one or more of any of the three medical conditions (Class 1), or none of the three medical conditions (Class 0). You will create a model trained on measurements of health characteristics.

To determine if someone has these medical conditions requires a long and intrusive process to collect information from patients. With predictive models, we can shorten this process and keep patient details private by collecting key characteristics relative to the conditions, then encoding these characteristics.

Your work will help researchers discover the relationship between measurements of certain characteristics and potential patient conditions.

## Context

They say age is just a number but a whole host of health issues come with aging. From heart disease and dementia to hearing loss and arthritis, aging is a risk factor for numerous diseases and complications. The growing field of bioinformatics includes research into interventions that can help slow and reverse biological aging and prevent major age-related ailments. Data science could have a role to play in developing new methods to solve problems with diverse data, even if the number of samples is small.

You could help advance the growing field of bioinformatics and explore new methods to solve complex problems with diverse data.

### Evaluation

Submissions are evaluated using a **balanced logarithmic loss** . The overall effect is such that each class is roughly equally important for the final score.

Each observation is either of class `0` or of class `1`. For each observation, you must submit a probability for each class. The formula is then:

## Submission File

For each  `id` in the test set, you must predict a probability for each of the two classes. The file should contain a header and have the following format:

```
Id,class_0,class_1
00eed32682bb,0.5,0.5
010ebe33f668,0.5,0.5
02fa521e1838,0.5,0.5
040e15f562a2,0.5,0.5
046e85c7cc7f,0.5,0.5
...
```
