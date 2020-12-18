# TODO
# Kaggle API for Dataset 
# Build connection to send csv data file
# Serve backend locally 
# Cleanse netflix dataset seperately

import pandas as pd 
import numpy as np 

# Date ranger spanning 2020
start_date = "2020-01-01"
end_date = "2021-01-01"

netflix_df = pd.read_csv('netflix_titles.csv') # 6234 rows
# Split dataset between shows and movies 
netflix_shows = netflix_df[netflix_df['type']=='TV Show'] # 1969 rows
netflix_movies = netflix_df[netflix_df['type']=='Movie'] # 4265 rows

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
# TODO - Drop Shows and Len column from movies
# movies.drop(['Shows', 'len'], axis=1, inplace=True)
# shows.drop(['Shows', 'len'], axis=1, inplace=True)

# Build new columns for Shows - Title, Season, Episode
# shows['title'], shows['season'], shows['episode'] = shows['Title'].str.split(':', 2).str
shows = shows.join(shows['Title'].str.split(':', 2, expand=True).rename(columns={0:'title', 1:'season', 2:'episode'}))


shows_collected = shows.groupby(['title']).apply(list).reset_index()
print(shows_collected)



# for col in netflix_df.columns:
#     print(col) 
#     print(netflix_df.head()[col])
#     print(" ")

# shows_collected.to_csv('out.csv', sep='\t')
