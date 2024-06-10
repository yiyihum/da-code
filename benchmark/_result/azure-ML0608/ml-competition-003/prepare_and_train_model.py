import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import log_loss
from sklearn.preprocessing import StandardScaler

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocessing
# Separate features and target variables
X = train_data.drop(['id', 'Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults'], axis=1)
y = train_data[['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']]

# Convert categorical variables to dummy variables
X = pd.get_dummies(X)

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier for each target variable
log_losses = []
for column in y.columns:
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train[column])
    
    # Validate the model
    y_val_pred_proba = clf.predict_proba(X_val)[:, 1]  # Get the probability for class 1
    log_loss_value = log_loss(y_val[column], y_val_pred_proba)
    log_losses.append(log_loss_value)

# Output the log losses for each condition
print('Log Losses for each condition:', log_losses)
