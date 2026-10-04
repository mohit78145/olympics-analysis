import pandas as pd

def preprocess(df1,region_df):
    df1 = df1[df1['Season'] == 'Summer']
    df1 = df1.merge(region_df, on='NOC', how='left')
    df1.drop_duplicates(inplace=True)
    df1 = pd.concat([df1, pd.get_dummies(df1['Medal']).astype(int)], axis=1)
    return df1