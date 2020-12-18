import pandas as pd 
import numpy as np 
import datetime

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


# ----------------- Basic Stats

# Total Time
totalTime_sec = int(df['Duration (s)'].sum())
totalTime_str = datetime.timedelta(seconds=totalTime_sec)

# Movies
num_movies = int(df.loc[df['Type']=='Movie', 'Type'].count())
duration_movies_sec = int(df.loc[df['Type']=='Movie', 'Duration (s)'].sum())
duration_movies_str = datetime.timedelta(seconds=duration_movies_sec)

# Shows 
num_shows = int(df.loc[df['Type']=='Serie', 'Type'].count())
duration_shows_sec = int(df.loc[df['Type']=='Serie', 'Duration (s)'].sum())
duration_shows_str = datetime.timedelta(seconds=duration_shows_sec)

# Day-by-Day
per_day = df.groupby(['day_of_week'], as_index=False).sum()
per_day['avg'] = (per_day['Duration (s)']/totalTime_sec)*100
per_day = per_day[['day_of_week', 'avg']]
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
    days[day] = float(per_day.loc[per_day['day_of_week']==day, 'avg'])

print(days)