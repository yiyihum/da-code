
## Overview

### Description

Essay writing is a critical method for assessing student learning and performance, yet manually grading essays is time-consuming for educators. Automated Writing Evaluation (AWE) systems aim to supplement this effort by scoring essays and providing timely feedback to students. However, these systems often come with high costs, limiting their accessibility to broader educational communities. This competition seeks to advance automated essay scoring by leveraging a comprehensive dataset that includes diverse samples aligned with current educational standards.

### Context

The first automated essay scoring competition, hosted twelve years ago, marked a significant milestone in exploring machine learning's role in grading student-written essays. This updated competition aims to build upon past achievements, offering a dataset enriched with high-quality, realistic classroom writing samples. By incorporating economic and geographic diversity, the dataset aims to mitigate potential algorithmic biases present in earlier efforts.

### Goals

Participants in this competition are tasked with developing open-source algorithms for essay scoring, improving upon previous initiatives like the Automated Student Assessment Prize (ASAP) competition of 2012. Hosted by Vanderbilt University in partnership with The Learning Agency Lab, this initiative aims to democratize access to robust AWE solutions. Winning solutions will be released as open source, ensuring widespread availability and support for educators, particularly in underserved districts.

### Evaluation

Submissions will be evaluated based on the quadratic weighted kappa, measuring agreement between predicted and actual essay scores. This metric ranges from 0 (random agreement) to 1 (perfect agreement), with negative values indicating less agreement than expected by chance.

### Submission File

For each essay_id in the test set, participants are required to predict the corresponding score. The submission file should follow this format:

```
essay_id,score
000d118,3
000fe60,3
001ab80,4
...
```

### Acknowledgments

Vanderbilt University and The Learning Agency Lab acknowledge the support of the Bill & Melinda Gates Foundation, Schmidt Futures, and Chan Zuckerberg Initiative for their contributions to this initiative.
