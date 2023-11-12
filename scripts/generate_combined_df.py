from pandas import concat, read_csv
import glob
import os

if (os.path.exists('../data/full_dataset.csv')):
    os.remove('../data/full_dataset.csv')

df_list = []
for dirname, _, filenames in os.walk('../data/'):
    for filename in filenames:
        file = os.path.join(dirname, filename)
        if file.endswith('.csv'):
            print(file)
            df_tmp = read_csv(file)
            df_list.append(df_tmp)
df = concat(df_list, axis=0).drop_duplicates()

# ## For first assignment ##
# selected_columns = ['scientific_name', 'common_name', 'city', 'state', 'height_M']
# df = df[selected_columns]


## For second assignment ##
selected_columns = ['scientific_name', 'common_name', 'city', 'state', 'height_M', 'diameter_breast_height_CM']
df = df[selected_columns]

df.to_csv('../data/full_dataset.csv', index=False)

df.info()