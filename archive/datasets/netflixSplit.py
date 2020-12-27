import pandas as pd 
import numpy as np 

netflix_df = pd.read_csv('netflix_titles.csv') # 6234 rows
# Split dataset between shows and movies 
netflix_shows = netflix_df[netflix_df['type']=='TV Show'] # 1969 rows
netflix_movies = netflix_df[netflix_df['type']=='Movie'] # 4265 rows

# Avg Runtime data from IMDB for movies and shows
imdb_shows = pd.read_csv('imdb_show.csv', header=0, escapechar='\\')
imdb_movies = pd.read_csv('imdb_movies.csv', header=0, escapechar='\\')

netflix_shows['release_year'] = netflix_shows['release_year'].astype(str)
# imdb_movies['release_year'] = imdb_movies['release_year'].astype(int)

# Merged df for shows and movies 
netflix_shows_rt = pd.merge(netflix_shows, imdb_shows, left_on=['title', 'release_year'], right_on=['title','startYear'], how='left')
# netflix_shows_rt['runtimeMinutes'].fillna(22.0)
netflix_movies_rt = pd.merge(netflix_movies, imdb_movies, on='title', how='left')




print(netflix_shows_rt[netflix_shows_rt['title']=='Friends'])


# print(netflix_shows_rt)
# print(netflix_movies_rt)

# Export data
# netflix_shows_rt.to_csv('netflix_shows.csv', sep=',')
# netflix_movies_rt.to_csv('netflix_movies.csv', sep=',')

