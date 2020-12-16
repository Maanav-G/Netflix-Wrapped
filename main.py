# TODO
# Kaggle API for Dataset 
# Build connection to send csv data file
# Serve backend locally 

import pandas as pd 
import numpy as np 

# Date ranger spanning 2020
start_date = "2020-01-01"
end_date = "2021-01-01"

df = pd.read_csv('NetflixViewingHistory.csv')

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
movies.drop(['Shows', 'len'], axis=1, inplace=True)
shows.drop(['Shows', 'len'], axis=1, inplace=True)

# Build new columns for Shows - Title, Season, Episode
# shows['title'], shows['season'], shows['episode'] = df['Title'].str.split(':', 2).str


netflix_df = pd.read_csv('netflix_titles.csv')
print(netflix_df.head())

# shows.to_csv('out.csv', sep='\t')
# print(shows)