## Dataset Description

The competition data comprises 110 mathematics problems similar in style to those of the** **[AIME](https://artofproblemsolving.com/wiki/index.php/AIME_Problems_and_Solutions).
The answer to each problem is a non-negative integer, which you should report modulo 1000. If, for instance, you believe the answer to a problem is** **`2034`, your prediction should be** **`34`.
You should expect the difficulty of the problems to be a bit easier than AIME and targeted between AIME and** **[AMC&#39;12](https://artofproblemsolving.com/wiki/index.php/AMC_12_Problems_and_Solutions) level.
All problems are text-only with mathematical notation in LaTeX. Please see the** **`AIMO Prize - Note on Language and Notation.pdf` handout for details on the notational conventions used. Although some problems may involve geometry, diagrams are not used in any problem.
The public test set comprises exactly 50 problems, and the private test set comprises a distinct set of 50 problems. We also provide a selection of 10 problems for use as training data. The problems in the two test sets have been selected to balance both difficulty and subject area.
Please note that this is a** **[Code Competition](https://www.kaggle.com/c/ai-mathematical-olympiad-prize/overview/code-requirements). We give a few placeholder problems in the publicly visible** **`test.csv` file to help you author your submissions. These problems are not meant to be representative of the problems in the actual test set. When your submission is scored, this placeholder test data will be replaced with the actual test data.
Because of the limited number of problems available, we are taking special precautions to secure the test set against probing. Among other things, during the submission period the test set will comprise only the 50 public set problems. Once the competition ends, when we rerun submissions, the test set will comprise only the 50 private set problems.** ** **You should attempt to make sure your submission will complete successfully on the 50 new private set problems.** This may mean ensuring your submission is robust to unexpected inputs, or managing runtime and memory usage.

## Fields

* `id` - A unique identifier for each problem.
* `problem` - A statement of the problem to be solved.
