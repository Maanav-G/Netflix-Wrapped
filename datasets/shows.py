import pandas as pd 
import numpy as np 

netflix_df = pd.read_csv('netflix_titles.csv') # 6234 rows
# Split dataset between shows and movies 
netflix_shows = netflix_df[netflix_df['type']=='TV Show'] # 1969 rows

# Avg Runtime data from IMDB
runtimes_df = pd.read_csv('runtime.csv', header=0, escapechar='\\')

# Merged df for shows
netflix_shows_rt = pd.merge(netflix_shows, runtimes_df, on='title', how='outer').fillna(22.0)

# Export data
netflix_shows_rt = pd.DataFrame(netflix_shows_rt, columns=['values'])
netflix_shows_rt.to_csv('netflix_shows.csv', sep=',')
