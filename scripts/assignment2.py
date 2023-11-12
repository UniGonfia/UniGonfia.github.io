import pandas as pd

df = pd.read_csv('../data/full_dataset.csv', low_memory=False)

df_grouped = df.groupby(['city', 'scientific_name']).agg({'scientific_name': 'count', 'height_M': 'mean', 'diameter_breast_height_CM': 'mean'})\
        .rename(columns={'scientific_name': 'count', 'height_M': 'mean_height', 'diameter_breast_height_CM': 'mean_diameter'})\
        .reset_index()

df_state = df[['city', 'state']].drop_duplicates()
df_grouped = pd.merge(df_grouped, df_state, on='city', how='outer')

df_grouped.to_json('../src/lib/data/assignment2.json', orient='records')