import numpy as np
def pearson_r(x, y):
    """Compute Pearson correlation coefficient between two arrays."""
    # Compute correlation matrix: corr_mat
    corr_mat = np.corrcoef(x, y)

    # Return entry [0,1]
    return corr_mat[0,1]

import pandas as pd

# Read the CSV file
df = pd.read_csv('../female_literacy_fertility.csv')

# Get the 'female literacy' column and convert it to a numerical format
literacy = pd.to_numeric(df['female literacy'], errors='coerce')

# Get the 'fertility' column
fertility = df['fertility']

# Calculate iliteracy
iliteracy = 100 - literacy

# If you want the results as numpy arrays:
import numpy as np
literacy_array = np.array(literacy)
fertility_array = np.array(fertility)
illiteracy_array = np.array(iliteracy)
# Show the Pearson correlation coefficient
print(pearson_r(illiteracy_array, fertility_array))

df = pd.DataFrame(
    {
        "result": [pearson_r(illiteracy_array, fertility_array)]
    }
)

df.to_csv("result.csv", index=False)
df["result"] = [""]
df.to_csv("../result.csv", index=False)
