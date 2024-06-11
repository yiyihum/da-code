import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Set up the matplotlib figure
sns.set(style="whitegrid")

# Histograms for feature distributions
features = ['Length', 'Diameter', 'Height', 'Weight', 'Shucked Weight', 'Viscera Weight', 'Shell Weight']
for feature in features:
    plt.figure(figsize=(10, 4))
    sns.histplot(train_data[feature], kde=True)
    plt.title(f'Distribution of {feature}')
    plt.show()

# Boxplot for target variable 'Age'
plt.figure(figsize=(10, 4))
sns.boxplot(x=train_data['Age'])
plt.title('Boxplot of Age')
plt.show()

# Pair plot to observe relationships between features and target variable
sns.pairplot(train_data[features + ['Age']])
plt.show()
