## Overview

**Welcome to the 2023 Kaggle Playground Series!** Thank you to everyone who participated in and contributed to Season 3 Playground Series so far!** **

**Your Goal:** For this Episode of the Series, your task is to use binary classification to predict a patient's smoking status given information about various other health indicators. Good luck!

### Evaluation

Submissions are evaluated on** **[area under the ROC curve](http://en.wikipedia.org/wiki/Receiver_operating_characteristic) between the predicted probability and the observed target.

## Submission File

For each** **`id` in the test set, you must predict the probability for the target variable** **`smoking`. The file should contain a header and have the following format:

```
id,smoking
159256,0.5
159257,0.5
159258,0.5
etc.
```
