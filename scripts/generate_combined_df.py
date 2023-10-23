from pandas import concat, read_csv
import glob

df = concat([read_csv(filepath_or_buffer=input_file, parse_dates=['most_recent_observation', 'planted_date', 'retired_date'],
                      low_memory=False,) for input_file in glob.glob('../data/*.csv')])

## For first assignment ##
# colums_to_remove = ['native', 'most_recent_observation', 'city_ID', 'tree_ID', 'planted_date', 'most_recent_observation_type',
#                     'retired_date', 'longitude_coordinate', 'latitude_coordinate', 'neighborhood', 'ward', 'zipcode', 'district', 'address',
#                     'location_name', 'percent_population', 'location_type', 'greater_metro']
# df.drop(colums_to_remove, axis=1, inplace=True)


df.to_csv('../data/full_dataset.csv', index=False)
