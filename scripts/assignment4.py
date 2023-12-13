import pandas as pd
import os

df = pd.read_csv('../data/tree/full_dataset.csv', low_memory=False)

df.dropna(subset=['longitude_coordinate', 'latitude_coordinate'], inplace=True)
df.dropna(subset=['scientific_name'], inplace=True)
df.dropna(subset=['neighborhood'], inplace=True)

#take only the coordinate
df = df[['longitude_coordinate', 'latitude_coordinate']]

#rename columns
df.rename(columns={'longitude_coordinate': 'ln', 'latitude_coordinate': 'la'}, inplace=True)

#to json
df.to_json('../src/lib/data/tree_coordinates.json', orient='records')