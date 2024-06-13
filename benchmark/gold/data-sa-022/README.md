### Explain the purpose of the uploaded code

#### Notebook name: `probability-density-functions.ipynb`

The purpose of this Jupyter notebook is to introduce and calculate the probability density function (PDF). Specific contents include:

1. **Overview of Probability Density Function**:
- Introduce a fictional class of students and their math test scores, ranging from 0 to 20, including fractional scores.
- Explain why the score is a continuous random variable and how to calculate the probability of a score within a specific range.

2. **Formula Derivation**:
- Explain how to calculate the probability of a score within a specific range through the formula \( P(11<x<20) = \frac{n(E)}{n(S)} \).
- Due to the infinite possibilities of continuous values ​​in reality, this direct counting method is not feasible, so the probability density function is introduced.

3. **Calculation of Probability Density Function**:
- The probability density function \( P(x) \) represents the probability of a random variable near a certain value, and can calculate the probability of the variable falling within a certain interval.
- Calculate the probability of a grade between 11 and 12 by integrating \( \int_{11}^{12}p(x)dx \) where \( p(x) \) is a given probability density function.

4. **Example calculation**:
- Given a specific probability density function \( \frac{1}{\sqrt{2\pi }}e^{-\frac{(x-10)^2}{2}} \) .
- Calculate the integral \( \int_{11}^{12}p(x)dx \) to determine the probability of a grade between 11 and 12.

Through theoretical explanations, formula derivations, and practical calculations, the notebook helps readers understand and apply probability density functions to solve practical problems.

### Question

How do you use a probability density function to calculate the probability of a continuous random variable in a specific interval and solve this probability by integration?