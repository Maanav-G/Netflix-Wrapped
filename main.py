# TODO
# Kaggle API for Dataset 
# Build connection to send csv data file
# Serve backend locally 

import pandas as pd 
import numpy as np 

# Date range spanning 2020
start_date = "2020-01-01"
end_date = "2021-01-01"

# Netflix shows and movies dataset
netflix_shows = pd.read_csv(r'./datasets/netflix_shows.csv') # 1969 rows
netflix_movies = pd.read_csv(r'./datasets/netflix_movies.csv') # 4265 rows

# User's viewing history
df = pd.read_csv(r'NetflixViewingHistory.csv')

# Get watch history for specified year
dates = df[df.Date >= start_date]
df = dates[dates.Date <= end_date]

# Devise new column for day of week
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['day_of_week'] = df['Date'].dt.day_name() # df['day_of_week'] = df['Date'].dt.weekday
df['month'] = df['Date'].dt.month_name() # df['day_of_week'] = df['Date'].dt.month


# Split between TV shows and movies based on title 
df['Shows'] = df['Title'].str.split(':',2)
df['len'] = df['Shows'].str.len()
shows = df[df['len'] == 3]
movies = df[df['len'] != 3]
# TODO - Drop Shows and Len column from movies
# movies.drop(['Shows', 'len'], axis=1, inplace=True)
# shows.drop(['Shows', 'len'], axis=1, inplace=True)

# Build new columns for Shows - Title, Season, Episode
shows = shows.join(shows['Title'].str.split(':', 2, expand=True).rename(columns={0:'title', 1:'season', 2:'episode'}))
movies['title'] = movies['Title']

# Add runtime for shows
shows_rt = pd.merge(shows, netflix_shows, on='title', how='left')
# Add runtime for movies
movies_rt = pd.merge(movies, netflix_movies, on='title', how='left')
print(shows_rt)

# Collect shows 
# shows_collected = shows.groupby(['title']).apply(list).reset_index()




# for col in netflix_df.columns:
#     print(col) 
#     print(netflix_df.head()[col])
#     print(" ")

# shows_collected.to_csv('out.csv', sep='\t')
