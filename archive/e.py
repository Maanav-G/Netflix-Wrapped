# Date range spanning 2020
start_date = "2020-01-01"
end_date = "2021-01-01"

# # Netflix shows and movies dataset
# netflix_shows = pd.read_csv(r'./datasets/netflix_shows.csv') # 1969 rows
# netflix_movies = pd.read_csv(r'./datasets/netflix_movies.csv') # 4265 rows

# User's viewing history
df = pd.read_csv(r'activity.csv')

# Get watch history for specified year
dates = df[df.Timestamp >= start_date]
df = dates[dates.Timestamp <= end_date]

# Devise new column for day of week
df['Date'] = pd.to_datetime(df['Timestamp'], errors='coerce')
df['day_of_week'] = df['Date'].dt.day_name() # df['day_of_week'] = df['Date'].dt.weekday
df['month'] = df['Date'].dt.month_name() # df['day_of_week'] = df['Date'].dt.month

# Build new columns for Shows - Title, Season, Episode
df = df.join(
    df['Title'].str.split('-', 1, expand=True)
    .rename(columns={0:'show_title', 1:'show_excess'})
    )









import pandas as pd 
import numpy as np 
import datetime

# User's viewing history
movies = pd.read_csv(r'activity_movies.csv')
shows = pd.read_csv(r'activity_shows.csv')
# df = pd.concat([movies, shows])


# ----------------- Basic Stats

# Total Unique Titles
# df_movies = movies[movies['Type']=='Movie']
grouped_titles_movies = movies['title'].value_counts()
# df_shows = df[df['Type']=='Serie']
grouped_titles_shows = shows['title'].value_counts()


# Movies
# num_movies = int(df.loc[df['Type']=='Movie', 'Type'].count())
# duration_movies_sec_ = int(df.loc[df['Type']=='Movie', 'Duration (s)'].sum())
#  ======
duration_movies_sec = int(movies['runtimeMinutes'].sum())
duration_movies_str = datetime.timedelta(minutes=duration_movies_sec)

# # Shows 
# num_shows = int(df.loc[df['Type']=='Serie', 'Type'].count())
duration_shows_sec = int(shows['runtimeMinutes'].sum())
duration_shows_str = datetime.timedelta(minutes=duration_shows_sec)


# Total Time
totalTime_sec = duration_movies_sec
totalTime_str = datetime.timedelta(seconds=totalTime_sec)

# # Day-by-Day
# per_day = df.groupby(['day_of_week'], as_index=False).sum()
# per_day['avg'] = (per_day['Duration (s)']/totalTime_sec)*100
# per_day = per_day[['day_of_week', 'avg']]
# days = {
#     "Monday":0,
#     "Tuesday":0,
#     "Wednesday":0,
#     "Thursday":0,
#     "Friday":0,
#     "Saturday":0,
#     "Sunday":0,
# }
# for day in days:
#     days[day] = float(per_day.loc[per_day['day_of_week']==day, 'avg'])
