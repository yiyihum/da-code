In this notebook, we investigate a polynomial of the form:

$$
\prod_{i=1}^{m} (1 + t^{2i + 1}) = (1 +t^3)(1+t^5)(1+t^7)...
$$

and verify that the distribution of its coefficients conforms to a normal distribution up to a certain precision.

This polynomial is the Poincare polynomial (a generating function for the dimensions of the cohomologies) for the $\mathit{SU}(m)$ group. We use SymPy to obtain the coefficients, and subsequently write the coefficients and the fitted normal distribution values to a CSV file.

Here are the parameters for our analysis:

- start_degree = 10
- end_degree = 30
- step = 5

Here's a brief explanation of the columns in the CSV file:

- **Degree**: The degree of each term in the polynomial.
- **Coefficient**: The coefficient of the polynomial for the corresponding degree.
- **Fitted_Normal_PDF**: The value of the normal distribution's PDF at the corresponding degree, fitted to match the distribution of the polynomial coefficients.

---

### Introduction to `polynomial_values.csv`

The `polynomial_values.csv` file contains the evaluated values of a specific polynomial of the form:

\[ P(t) = \prod_{i=1}^{m} (1 + t^{2i + 1}) \]

For this file, the polynomial was generated with \( m = 5 \), resulting in the product:

\[ P(t) = (1 + t^3)(1 + t^5)(1 + t^7)(1 + t^9)(1 + t^{11}) \]

The file provides the polynomial values evaluated at 100 equally spaced points within the range of \(-10\) to \(10\). This data helps to visualize and analyze the behavior of the polynomial over a specified range of \( t \) values.

### Columns

The CSV file consists of two columns:

1. **t_value**: This column represents the \( t \) values at which the polynomial is evaluated. These values range from \(-10\) to \(10\), inclusive, with 100 equally spaced points.
2. **polynomial_value**: This column contains the corresponding values of the polynomial \( P(t) \) evaluated at each \( t \) value.

### Sample Data

The first few rows of the file look like this:

| t_value | polynomial_value |
| ------- | ---------------- |
| -10.0   | ...              |
| -9.8    | ...              |
| -9.6    | ...              |
| -9.4    | ...              |
| ...     | ...              |

### Usage

This file can be used for various purposes, such as:

- **Visualization**: Plotting the polynomial values against \( t \) values to understand the polynomial's behavior.
- **Analysis**: Studying the properties of the polynomial and how it changes with different \( t \) values.
- **Educational**: Demonstrating the process of polynomial generation and evaluation in a mathematical or programming context.

This introduction should provide a clear understanding of the contents and purpose of the `polynomial_values.csv` file.
