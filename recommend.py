import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from math import sqrt


def delete_duplicate(row):
    return list(set(row))


def delete_space(row):
    for i in range(0, len(row)):
        row[i] = row[i].replace(" ", "")
    return row


def convert_to_dataframe(df):
    return pd.DataFrame(df)


def preprocessing(df):
    # delete duplicates
    df['purpose'] = df['purpose'].apply(delete_duplicate)
    df['interest'] = df['interest'].apply(delete_duplicate)

    # delete space
    df['purpose'] = df['purpose'].apply(delete_space)
    df['interest'] = df['interest'].apply(delete_space)

    # convert to literal
    df['purpose'] = df['purpose'].apply(lambda x : (' ').join(x))
    df['interest'] = df['interest'].apply(lambda x : (' ').join(x))

    return df


def get_results(df, id):
    df = convert_to_dataframe(df)
    df = preprocessing(df)

    # CountVectorizer
    count_vect = CountVectorizer(min_df=0, ngram_range=(1, 1))
    purpose_mat = count_vect.fit_transform(df['purpose'])
    interest_mat = count_vect.fit_transform(df['interest'])

    # calculate cosine similarity
    purpose_sim = cosine_similarity(purpose_mat, purpose_mat)
    interest_sim = cosine_similarity(interest_mat, interest_mat)

    # specific user profile
    profile = df[df['id'] == id]
    profile_idx = profile.index.values

    # add similarity column
    df["purpose_similarity"] = purpose_sim[profile_idx, :].reshape(-1, 1)
    df["interest_similarity"] = interest_sim[profile_idx, :].reshape(-1, 1)

    my_purpose = df.iloc[profile_idx[0], 1]

    if '친목' in my_purpose:
        minmax_scaler = MinMaxScaler()
        my_lat = df.loc[profile_idx]['latitude']
        my_long = df.loc[profile_idx]['longitude']
        df['distance'] = df.apply(lambda x : sqrt((my_lat - x['latitude'])**2 + (my_long - x['longitude'])**2), axis=1)
        df['distance_similarity'] = (1 - minmax_scaler.fit_transform(df[['distance']]))
        df['similarity'] = 0.1*df['purpose_similarity'] + 0.6*df['interest_similarity'] + 0.3*df['distance_similarity']
        df = df.sort_values(by="similarity", ascending=False)
        return df['id'].to_list()
    elif '한국생활적응' in my_purpose:
        minmax_scaler = MinMaxScaler()
        df['rperiod_similarity'] = minmax_scaler.fit_transform(df[['rperiod']])
        df['rperiod_similarity'].apply(lambda x : 1 - x)
        df['similarity'] = 0.2*df['purpose_similarity'] + 0.2*df['interest_similarity'] + 0.6*df['rperiod_similarity']
        df = df.sort_values(by="similarity", ascending=False)
        return df['id'].to_list()
    elif '육아정보공유' in my_purpose or '한국어공부' in my_purpose:
        df['similarity'] = 0.2*df['purpose_similarity'] + 0.8*df['interest_similarity']
        df = df.sort_values(by="similarity", ascending=False)
        return df['id'].to_list()

