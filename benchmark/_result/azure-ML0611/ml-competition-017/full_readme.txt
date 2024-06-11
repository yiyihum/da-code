## Overview

The first** **[automated essay scoring competition](https://www.kaggle.com/competitions/asap-aes/overview) to tackle automated grading of student-written essays was twelve years ago. How far have we come from this initial competition? With an updated dataset and light years of new ideas we hope to see if we can get to the latest in automated grading to provide a real impact to overtaxed teachers who continue to have challenges with providing timely feedback, especially in underserved communities.** **

The goal of this competition is to train a model to score student essays. Your efforts are needed to reduce the high expense and time required to hand grade these essays. Reliable automated techniques could allow essays to be introduced in testing, a key indicator of student learning that is currently commonly avoided due to the challenges in grading.

Start

2 months ago

###### Close

a month to go

Merger & Entry

### Description

link

keyboard_arrow_up

Essay writing is an important method to evaluate student learning and performance. It is also time-consuming for educators to grade by hand. Automated Writing Evaluation (AWE) systems can score essays to supplement an educator’s other efforts. AWEs also allow students to receive regular and timely feedback on their writing. However, due to their costs, many advancements in the field are not widely available to students and educators. Open-source solutions to assess student writing are needed to reach every community with these important educational tools.
Previous efforts to develop open-source AWEs have been limited by small datasets that were not nationally diverse or focused on common essay formats. The first Automated Essay Scoring competition scored student-written short-answer responses, however, this is a writing task not often used in the classroom. To improve upon earlier efforts, a more expansive dataset that includes high-quality, realistic classroom writing samples was required. Further, to broaden the impact, the dataset should include samples across economic and location populations to mitigate the potential of algorithmic bias.
In this competition, you will work with the largest open-access writing dataset aligned to current standards for student-appropriate assessments. Can you help produce an open-source essay scoring algorithm that improves upon the original** **[Automated Student Assessment Prize (ASAP)](https://www.kaggle.com/competitions/asap-aes/overview) competition hosted in 2012?** **
Competition host Vanderbilt University is a private research university in Nashville, Tennessee. For this competition, Vanderbilt has partnered with The Learning Agency Lab, an Arizona-based independent nonprofit focused on developing the science of learning-based tools and programs for the social good.
To ensure the results of this competition are widely available, winning solutions will be released as open source. More robust and accessible AWE options will help more students get the frequent feedback they need and provide educators with additional support, especially in underserved districts.

### Acknowledgments

Vanderbilt University and the Learning Agency Lab would like to thank the Bill & Melinda Gates Foundation, Schmidt Futures, and Chan Zuckerberg Initiative for their support in making this work possible.** **
[![img](https://storage.googleapis.com/kaggle-media/competitions/The%20Learning%20Agency/BMGF_logo_black_300dpi%20(1).jpg)         ](https://www.gatesfoundation.org/)[![](https://storage.googleapis.com/kaggle-media/competitions/The%20Learning%20Agency/Schmidt%20Futures%20Logo.png)        ](https://schmidtfutures.com/)

[
    ](https://chanzuckerberg.com/)Evaluation

Submissions are scored based on the quadratic weighted kappa, which measures the agreement between two outcomes. This metric typically varies from 0 (random agreement) to 1 (complete agreement). In the event that there is less agreement than expected by chance, the metric may go below 0.

The quadratic weighted kappa is calculated as follows. First, an N x N histogram matrix** ***O* is constructed, such that** ***O~i,j~* corresponds to the number of** **`essay_id`s** ***i* (actual) that received a predicted value** ** *j* . An** ***N-by-N** ***matrix of weights,** ** *w* , is calculated based on the difference between actual and predicted values:

**𝑤**𝑖**,**𝑗**=**(**𝑖**−**𝑗**)**2**(**𝑁**−**1**)**2**

An** ***N-by-N* histogram matrix of expected outcomes,** ** *E* , is calculated assuming that there is no correlation between values. ** **
This is calculated as the outer product between the actual histogram vector of outcomes and the predicted histogram vector, normalized such that** ***E* and** ***O* have the same sum.

From these three matrices, the quadratic weighted kappa is calculated as:

**𝜅**=**1**−**∑**𝑖**,**𝑗**𝑤**𝑖**,**𝑗**𝑂**𝑖**,**𝑗**∑**𝑖**,**𝑗**𝑤**𝑖**,**𝑗**𝐸**𝑖**,**𝑗**.**

## Submission File

For each** **`essay_id` in the test set, you must predict the corresponding** **`score` (described on the** **[Data](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/data) page). The file should contain a header and have the following format:

```
essay_id,score
000d118,3
000fe60,3
001ab80,4
...
```
