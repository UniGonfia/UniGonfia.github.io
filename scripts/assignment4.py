import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import json

# Read the CSV file
df = pd.read_csv('../data/tree/full_dataset.csv', low_memory=False)

# Select relevant columns
df_lat_lon = df[['city', 'state', 'longitude_coordinate', 'latitude_coordinate']]

# Drop duplicates and NaN values
df_lat_lon = df_lat_lon.drop_duplicates()
df_lat_lon = df_lat_lon.dropna()

# Define the number of bins for the bounding boxes
num_bins = 10  # Adjust this value based on your preference

# Create an empty list to store results
results = []

# Create bounding boxes for each state
for state in df_lat_lon['state'].unique():
    state_data = df_lat_lon[df_lat_lon['state'] == state]
    
    # Calculate the bounding box for the state
    lon_min, lon_max = state_data['longitude_coordinate'].min(), state_data['longitude_coordinate'].max()
    lat_min, lat_max = state_data['latitude_coordinate'].min(), state_data['latitude_coordinate'].max()
    
    # Create 2D histogram to count points in each bin
    hist_2d, lon_edges, lat_edges = np.histogram2d(
        state_data['longitude_coordinate'],
        state_data['latitude_coordinate'],
        bins=[np.linspace(lon_min, lon_max, num_bins + 1), np.linspace(lat_min, lat_max, num_bins + 1)]
    )
    
    # Calculate the density for each bin
    bin_areas = np.diff(lon_edges)[:, np.newaxis] * np.diff(lat_edges)[np.newaxis, :]
    density = hist_2d / bin_areas
    
    # Identify and combine boxes
    for i in range(num_bins):
        for j in range(num_bins):
            
            if hist_2d[i, j] == 0:
                continue
            
            bin_info = {
                'state': state,
                'city': f'Bin_{i}_{j}',
                'bounding_box': {
                    'lon_min': lon_edges[i],
                    'lon_max': lon_edges[i + 1],
                    'lat_min': lat_edges[j],
                    'lat_max': lat_edges[j + 1]
                },
                'num_points': int(hist_2d[i, j]),
                'middle_point': {
                    'longitude': (lon_edges[i] + lon_edges[i + 1]) / 2,
                    'latitude': (lat_edges[j] + lat_edges[j + 1]) / 2
                }
            }
            
            results.append(bin_info)

    


# Save results to a JSON file
with open('../src/lib/data/tree_density.json', 'w') as json_file:
    json.dump(results, json_file, indent=2)


df = pd.read_csv('../data/tree/full_dataset.csv', low_memory=False)

# find the top 10 species
top_10_species = df['scientific_name'].value_counts().head(10).index.tolist()

df_lat_lon = df[['city', 'state', 'scientific_name', 'longitude_coordinate', 'latitude_coordinate']]
df_lat_lon = df_lat_lon.dropna()

# Create an empty list to store results
results = []

num_bins = 10

for state in df_lat_lon['state'].unique():
    state_data = df_lat_lon[df_lat_lon['state'] == state]
    
    # Calculate the bounding box for the state
    lon_min, lon_max = state_data['longitude_coordinate'].min(), state_data['longitude_coordinate'].max()
    lat_min, lat_max = state_data['latitude_coordinate'].min(), state_data['latitude_coordinate'].max()
    
    # Create 2D histogram to count points in each bin
    hist_2d, lon_edges, lat_edges = np.histogram2d(
        state_data['longitude_coordinate'],
        state_data['latitude_coordinate'],
        bins=[np.linspace(lon_min, lon_max, num_bins + 1), np.linspace(lat_min, lat_max, num_bins + 1)]
    )
    
    # Calculate the density for each bin
    bin_areas = np.diff(lon_edges)[:, np.newaxis] * np.diff(lat_edges)[np.newaxis, :]
    
    # Identify and combine boxes
    for i in range(num_bins):
        for j in range(num_bins):
            
            if hist_2d[i, j] == 0:
                continue
            
        
            num_points = int(hist_2d[i, j])
            species_val = []
            for species in top_10_species:
                num_points_species = len(state_data[(state_data['scientific_name'] == species) & \
                                                    (state_data['longitude_coordinate'] >= lon_edges[i]) & \
                                                    (state_data['longitude_coordinate'] < lon_edges[i + 1]) & \
                                                    (state_data['latitude_coordinate'] >= lat_edges[j]) & \
                                                    (state_data['latitude_coordinate'] < lat_edges[j + 1])])
                if num_points_species == 0:
                    continue
                                
                species_val.append({
                    'scientific_name': species,
                    'num_points_species': num_points_species,
                })
                
                num_points -= num_points_species
                
            results.append({
                'state': state,
                'city': f'Bin_{i}_{j}',
                'bounding_box': {
                    'lon_min': lon_edges[i],
                    'lon_max': lon_edges[i + 1],
                    'lat_min': lat_edges[j],
                    'lat_max': lat_edges[j + 1]
                },
                'num_points': int(hist_2d[i, j]),
                'middle_point': {
                    'longitude': (lon_edges[i] + lon_edges[i + 1]) / 2,
                    'latitude': (lat_edges[j] + lat_edges[j + 1]) / 2
                },
                'species': species_val
            })
                
                
# Save results to a JSON file
with open('../src/lib/data/tree_density_species.json', 'w') as json_file:
    json.dump(results, json_file, indent=2)
    

df = pd.read_csv('../data/tree/full_dataset.csv', low_memory=False)

# Desnity for state
df_lat_lon = df[['city', 'state',]]
df_lat_lon = df_lat_lon.dropna()

# Create an empty list to store results
results = []

for state in df_lat_lon['state'].unique():
   results.append({
       'state': state,
       'num_trees': len(df_lat_lon[df_lat_lon['state'] == state])
   })
   
            
# Save results to a JSON file
with open('../src/lib/data/tree_density_state.json', 'w') as json_file:
    json.dump(results, json_file, indent=2)
