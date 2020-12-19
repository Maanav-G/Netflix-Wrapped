import pandas as pd 
import numpy as np 
import datetime

# User's viewing history
movies = pd.read_csv(r'activity_movies.csv')
shows = pd.read_csv(r'activity_shows.csv')
# df = pd.concat([movies, shows])


# ----------------- Basic Stats

# Total Unique Titles
grouped_titles_movies = movies['title'].value_counts()
grouped_titles_shows = shows['title'].value_counts()


# Movies
duration_movies_min = int(movies['runtimeMinutes'].sum())
duration_movies_str = datetime.timedelta(minutes=duration_movies_min)

# # Shows 
duration_shows_min = int(shows['runtimeMinutes'].sum())
duration_shows_str = datetime.timedelta(minutes=duration_shows_min)


# Total Time
totalTime_min = duration_movies_min + duration_shows_min
totalTime_str = datetime.timedelta(minutes=totalTime_min)

# Day-by-Day
per_day_shows = shows.groupby(['day_of_week'], as_index=False).sum()
per_day_shows['runtimeMinutes_s'] = per_day_shows['runtimeMinutes']
per_day_shows = per_day_shows[['day_of_week', 'runtimeMinutes_s']]
per_day_movies = movies.groupby(['day_of_week'], as_index=False).sum()
per_day_movies['runtimeMinutes_m'] = per_day_movies['runtimeMinutes']
per_day_movies = per_day_movies[['day_of_week', 'runtimeMinutes_m']]
per_day = pd.merge(per_day_shows, per_day_movies, on='day_of_week', how='outer').fillna(0)
per_day['runtimeMinutes_t'] = per_day['runtimeMinutes_s'] + per_day['runtimeMinutes_m']
days = {
    "Monday":0,
    "Tuesday":0,
    "Wednesday":0,
    "Thursday":0,
    "Friday":0,
    "Saturday":0,
    "Sunday":0,
}
for day in days:
    days[day] = float(per_day.loc[per_day['day_of_week']==day, 'runtimeMinutes_t'])