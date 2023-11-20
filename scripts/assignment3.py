import pandas as pd
import os

df_list = []
for dirname, _, filenames in os.walk('../data/temperature'):
    for filename in filenames:
        file = os.path.join(dirname, filename)
        if file.endswith('_t.txt'):
            df_tmp = pd.read_csv(file, header=None, engine='python', dtype=str, sep='\s+')
            df_list.append(df_tmp)
df = pd.concat(df_list, axis=0)

df.columns = ['code', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

df['city'] = df['code'].str[:3]
df['measurement'] = df['code'].str[3:6]
df['year'] = df['code'].str[6:]
df.drop('code', axis=1, inplace=True)

df['measurement'] = df['measurement'].replace({'002': 'avg', '027': 'max', '028': 'min'})

with open('../data/temperature/cities.txt') as f:
    cities = f.read().splitlines()
    for city in cities:
        code = city.split(' ')[0]
        city_name = city.split(' ')[1]
        df['city'] = df['city'].replace({code: city_name})


# Remove the rows with no city name so with a code like 115
df = df[df['city'].str.len() > 3]


# df types
df = df.astype({'jan': 'float64', 'feb': 'float64', 'mar': 'float64', 'apr': 'float64', 'may': 'float64', 'jun': 'float64', 
                'jul': 'float64', 'aug': 'float64', 'sep': 'float64', 'oct': 'float64', 'nov': 'float64', 'dec': 'float64', 
                'year': 'int64', 'city': 'string', 'measurement': 'string'})

# take only year 2020-2010-2000-1990-1980-1970-1960-1950-1940-1930
year_filter = [2020, 2010, 2000, 1990, 1980, 1970, 1960, 1950, 1940, 1930]
df = df[df['year'].isin(year_filter)]

# If the value of months is <= -99.90 then replace with the value of the previous year
for i in range(1, len(df)):
    for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
        if df[month].iloc[i] <= -99.90:
            df[month].iloc[i] = df[month].iloc[i-1]
            

import json

# Group by 'city', 'year' and calculate average, max, and min for each month
result = df.groupby(['city', 'year']).agg({
    'jan': ['mean', 'max', 'min'],
    'feb': ['mean', 'max', 'min'],
    'mar': ['mean', 'max', 'min'],
    'apr': ['mean', 'max', 'min'],
    'may': ['mean', 'max', 'min'],
    'jun': ['mean', 'max', 'min'],
    'jul': ['mean', 'max', 'min'],
    'aug': ['mean', 'max', 'min'],
    'sep': ['mean', 'max', 'min'],
    'oct': ['mean', 'max', 'min'],
    'nov': ['mean', 'max', 'min'],
    'dec': ['mean', 'max', 'min']
})

# Convert the result to the desired JSON structure
nested_json = {}

for (city, year), data in result.iterrows():
    city = str(city)  # Ensure city is a string
    year = int(year)   # Ensure year is an integer
    
    if city not in nested_json:
        nested_json[city] = {}

    nested_json[city][year] = {
        'jan': {'avg': data['jan']['mean'], 'max': data['jan']['max'], 'min': data['jan']['min']},
        'feb': {'avg': data['feb']['mean'], 'max': data['feb']['max'], 'min': data['feb']['min']},
        'mar': {'avg': data['mar']['mean'], 'max': data['mar']['max'], 'min': data['mar']['min']},
        'apr': {'avg': data['apr']['mean'], 'max': data['apr']['max'], 'min': data['apr']['min']},
        'may': {'avg': data['may']['mean'], 'max': data['may']['max'], 'min': data['may']['min']},
        'jun': {'avg': data['jun']['mean'], 'max': data['jun']['max'], 'min': data['jun']['min']},
        'jul': {'avg': data['jul']['mean'], 'max': data['jul']['max'], 'min': data['jul']['min']},
        'aug': {'avg': data['aug']['mean'], 'max': data['aug']['max'], 'min': data['aug']['min']},
        'sep': {'avg': data['sep']['mean'], 'max': data['sep']['max'], 'min': data['sep']['min']},
        'oct': {'avg': data['oct']['mean'], 'max': data['oct']['max'], 'min': data['oct']['min']},
        'nov': {'avg': data['nov']['mean'], 'max': data['nov']['max'], 'min': data['nov']['min']},
        'dec': {'avg': data['dec']['mean'], 'max': data['dec']['max'], 'min': data['dec']['min']}
    }

# Write the JSON to a file
with open('../src/lib/data/assignment3.json', 'w') as f:
    json.dump(nested_json, f, indent=3)