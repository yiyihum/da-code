import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def preprocess_data(train_data, test_data):
    # Convert 'first_day_of_month' to datetime and extract year and month
    train_data['first_day_of_month'] = pd.to_datetime(train_data['first_day_of_month'])
    train_data['year'] = train_data['first_day_of_month'].dt.year
    train_data['month'] = train_data['first_day_of_month'].dt.month
    test_data['first_day_of_month'] = pd.to_datetime(test_data['first_day_of_month'])
    test_data['year'] = test_data['first_day_of_month'].dt.year
    test_data['month'] = test_data['first_day_of_month'].dt.month

    # Drop 'first_day_of_month' and 'row_id' columns
    train_data = train_data.drop(['first_day_of_month', 'row_id'], axis=1)
    test_data = test_data.drop(['first_day_of_month'], axis=1)

    # One-hot encode 'county' and 'state' columns
    encoder = OneHotEncoder()
    encoder.fit(pd.concat([train_data[['county', 'state']], test_data[['county', 'state']]]))
    train_encoded_features = encoder.transform(train_data[['county', 'state']])
    test_encoded_features = encoder.transform(test_data[['county', 'state']])
    train_encoded_df = pd.DataFrame(train_encoded_features.toarray(), columns=encoder.get_feature_names_out(['county', 'state']))
    test_encoded_df = pd.DataFrame(test_encoded_features.toarray(), columns=encoder.get_feature_names_out(['county', 'state']))

    # Concatenate the original dataframes with the encoded dataframes
    train_data = pd.concat([train_data, train_encoded_df], axis=1)
    test_data = pd.concat([test_data, test_encoded_df], axis=1)

    # Drop 'county' and 'state' columns
    train_data = train_data.drop(['county', 'state'], axis=1)
    test_data = test_data.drop(['county', 'state'], axis=1)

    return train_data, test_data
