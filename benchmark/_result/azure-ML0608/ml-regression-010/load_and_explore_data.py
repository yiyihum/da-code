import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/drugsComTrain_raw.csv')

# Display basic information about the dataset
print(train_data.info())

# Display the distribution of the 'usefulCount' column
print(train_data['usefulCount'].describe())

# Display the distribution of the 'rating' column
print(train_data['rating'].describe())
