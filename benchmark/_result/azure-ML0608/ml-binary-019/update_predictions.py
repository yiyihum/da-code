import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the predictions
predictions_df = pd.read_csv('class.csv')

# Initialize the label encoder for the class
le = LabelEncoder()
le.classes_ = ['e', 'p']  # Assuming 0 is 'e' and 1 is 'p' based on typical alphabetical order

# Inverse transform the numeric predictions back to original labels
predictions_df['class'] = le.inverse_transform(predictions_df['class'])

# Save the updated predictions to class.csv
predictions_df.to_csv('class.csv', index=False)
