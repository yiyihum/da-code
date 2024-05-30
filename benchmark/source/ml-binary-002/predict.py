import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load the complete info data
complete_info_df = pd.read_csv('complete_info.csv')
# Process categorical data
cat_features = complete_info_df.select_dtypes(include=['object']).columns
le = LabelEncoder()
for feature in cat_features:
    complete_info_df[feature] = le.fit_transform(complete_info_df[feature])

# Separate features and target
X = complete_info_df.drop(['building_id', 'damage_grade'], axis=1)
y = complete_info_df['damage_grade']

# Train the model
clf = RandomForestClassifier()
clf.fit(X, y)

# Load the incomplete info data
incomplete_info_df = pd.read_csv('incomplete_info.csv')
# Process categorical data
for feature in cat_features:
    incomplete_info_df[feature] = le.fit_transform(incomplete_info_df[feature])

# Predict damage grades
incomplete_info_df['damage_grade'] = clf.predict(incomplete_info_df.drop(['building_id'], axis=1))

# Save the predictions to a new csv file
incomplete_info_df[['building_id', 'damage_grade']].to_csv('prediction.csv', index=False)