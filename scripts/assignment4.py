import pandas as pd
import os

df = pd.read_csv('../data/tree/full_dataset.csv', low_memory=False)

df.dropna(subset=['longitude_coordinate', 'latitude_coordinate'], inplace=True)
df.dropna(subset=['scientific_name'], inplace=True)

