import pandas as pd

df = pd.read_csv('../data/full_dataset.csv', low_memory=False)

grouped = df.groupby(['scientific_name', 'city', 'state'])['height_M'].agg(['count', 'mean']).reset_index()
grouped.sort_values(by=['mean'], inplace=True, ascending=False)

# Remove all rows with null values
grouped.dropna(inplace=True)

# Remove all rows with mean and count == 0
grouped = grouped[grouped['mean'] != 0]
grouped = grouped[grouped['count'] != 0]

# To csv
grouped.to_json('../src/lib/data/assignment1.json', orient='records')
