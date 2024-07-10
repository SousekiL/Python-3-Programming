# %%
# Visualizing Flight Paths with Python
# https://nbviewer.org/gist/paulgb/5851489
import pandas as pd
import numpy as np
import os

os.chdir('/Users/sousekilyu/Documents/GitHub/Python-3-Programming/data/OpenFlights')

ROUTE_COLS = ('airline_name', 'airline_id', 'source_code', 'source_id', 'dest_code', 'dest_id', 'codeshare', 'stops', 'equiptment')
AIRPORT_COLS = ('airport_id', 'airport_name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude', 'altitude', 'timezone', 'dst')

routes = pd.read_csv('routes.dat', header=None, names=ROUTE_COLS, na_values=['\\N'])
airports = pd.read_csv('airports.dat', header=None, names=AIRPORT_COLS)

routes.head(10)
airports.head(10)

# %%
airport_pairs = routes.groupby(['source_code', 'dest_code']).size()
airport_pairs = airport_pairs.reset_index()
airport_pairs.columns = ['source_code', 'dest_code', 'cnt']

airport_pairs['source_code'] = airport_pairs['source_code'].astype(str)
airport_pairs['dest_code'] = airport_pairs['dest_code'].astype(str)

airport_pairs = airport_pairs.merge(airports, left_on='source_code', right_on='airport_name') \
                             .merge(airports, left_on='dest_code', right_on='airport_name', suffixes=('_source', '_dest'))

airport_pairs['longitude_source'] = pd.to_numeric(airport_pairs['longitude_source'], errors='coerce')
airport_pairs['latitude_source'] = pd.to_numeric(airport_pairs['latitude_source'], errors='coerce')
airport_pairs['longitude_dest'] = pd.to_numeric(airport_pairs['longitude_dest'], errors='coerce')
airport_pairs['latitude_dest'] = pd.to_numeric(airport_pairs['latitude_dest'], errors='coerce')
airport_pairs['cnt'] = pd.to_numeric(airport_pairs['cnt'], errors='coerce')

airport_pairs.head(10)

# %%
from gcmap import GCMapper
gcm = GCMapper()
gcm.set_data(airport_pairs.longitude_source, airport_pairs.latitude_source, airport_pairs.longitude_dest, airport_pairs.latitude_dest, airport_pairs.cnt)
img = gcm.draw()

img.save('test.png')

from IPython.core import display
display.Image(filename='test.png')

# %%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Create a map
fig = plt.figure(figsize=(20, 15))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Draw coastlines and borders
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)

# Plot flight paths
for _, row in airport_pairs.iterrows():
    plt.plot([row['longitude_source'], row['longitude_dest']], [row['latitude_source'], row['latitude_dest']],
             color='red', linewidth=2, transform=ccrs.Geodetic())  # Changed color to 'red' and linewidth to 2

# Save the map
plt.savefig('flight_paths.png')
plt.show()