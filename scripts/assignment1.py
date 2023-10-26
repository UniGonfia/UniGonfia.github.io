import pandas as pd

df = pd.read_csv('../data/full_dataset.csv', low_memory=False)


df_without_height = df.drop('height_M', axis=1)
df_without_height.dropna(inplace=True)
# Calculate the sum of city and scientific name occurrences in the dataset add a column with the sum
grouped_count = df_without_height.groupby('city')['scientific_name'].count().reset_index(name='count')

df_with_height = df
df_with_height.dropna(inplace=True)
# Calculate the mean of the height of the trees in each city
grouped_height = df_with_height.groupby('city')['height_M'].mean().reset_index(name='height_M')

# Merge the two dataframes if there isnt an height for a city put it equal to 0
grouped = pd.merge(grouped_count, grouped_height, on='city', how='outer')


grouped.sort_values(by=['count'], ascending=False, inplace=True)

print(grouped.head(20))


# To csv
grouped.to_json('../src/lib/data/assignment1.json', orient='records')
