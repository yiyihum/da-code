## Overview

**Welcome to the 2024 Kaggle Playground Series!** We plan to continue in the spirit of previous playgrounds, providing interesting an approachable datasets for our community to practice their machine learning skills, and anticipate a competition each month.

**Your Goal:** Predict the probability of various defects on steel plates. Good luck!

Start

Mar 1, 2024

###### Close

Apr 1, 2024

### Evaluation

link

keyboard_arrow_up

Submissions are evaluated using** **[area under the ROC curve](http://en.wikipedia.org/wiki/Receiver_operating_characteristic) using the predicted probabilities and the ground truth targets.

To calculate the final score, AUC is calculated for each of the 7 defect categories and then averaged. In other words, the score is the average of the individual AUC of each predicted column.

## Submission File

For each** **`id` in the test set, you must predict the probability for each of 7 defect categories:** **`Pastry`,** **`Z_Scratch`,** **`K_Scatch`,** **`Stains`,** **`Dirtiness`,** **`Bumps`,** **`Other_Faults`. The file should contain a header and have the following format:

```
id,Pastry,Z_Scratch,K_Scatch,Stains,Dirtiness,Bumps,Other_Faults
19219,0.5,0.5,0.5,0.5,0.5,0.5,0.5
19220,0.5,0.5,0.5,0.5,0.5,0.5,0.5
19221,0.5,0.5,0.5,0.5,0.5,0.5,0.5
etc.
```
