import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the preprocessed data
df = pd.read_csv('/workspace/preprocessed_test.csv')

# Separate features
X = df.drop(['Date', 'Location'], axis=1)

# Identify categorical columns that need to be encoded
categorical_cols = X.select_dtypes(include=['object']).columns

# Create a column transformer with OneHotEncoder for categorical variables
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'  # Leave the rest of the columns untouched
)

# Create a pipeline with preprocessing and the logistic regression model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('scaler', StandardScaler(with_mean=False)),  # with_mean=False to support sparse matrices
    ('model', LogisticRegression())
])

# Train the pipeline on the data
pipeline.fit(X, X['RainToday'])

# Make predictions on the same dataset
predictions = pipeline.predict(X)

# Save the predictions to a new CSV file
predictions_df = pd.DataFrame(predictions, columns=['RainTomorrow'])
predictions_df.to_csv('/workspace/tomorrow.csv', index=False)

# Print the first few rows of the predictions dataframe
print(predictions_df.head())
