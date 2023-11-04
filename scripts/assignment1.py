import pandas as pd

df = pd.read_csv('../data/full_dataset.csv', low_memory=False)


df_without_height = df.drop('height_M', axis=1)
# Calculate the sum of city and scientific name occurrences in the dataset add a column with the sum
grouped_count = df_without_height.groupby(['city', 'scientific_name'])['scientific_name'].count().reset_index(name='count')

df_with_height = df
# Calculate the mean of the height of the trees in each city
grouped_height = df_with_height.groupby(['city', 'scientific_name'])['height_M'].mean().reset_index(name='mean_height')

# Merge the two dataframes if there isnt an height for a city put it equal to 0
grouped = pd.merge(grouped_count, grouped_height, on=['city', 'scientific_name'], how='outer')

# Add the state according to the city the state is in the df

df_state = df[['city', 'state']].drop_duplicates()
grouped = pd.merge(grouped, df_state, on='city', how='outer')


grouped.sort_values(by=['count'], ascending=False, inplace=True)

# To json
grouped.to_json('../src/lib/data/assignment1.json', orient='records')