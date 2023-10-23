import pandas as pd

df = pd.read_csv('../data/full_dataset.csv', low_memory=False)

grouped = df.groupby(['scientific_name', 'city', 'state'])['height_M'].agg(['count', 'mean']).reset_index()
grouped.sort_values(by=['mean'], inplace=True, ascending=False)

# To csv
grouped.to_json('../src/lib/data/assignment1.json', orient='records')
