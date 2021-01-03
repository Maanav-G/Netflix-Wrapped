import json

# animal = {'type':'cat', 'age':12}
# print(animal)
# as_json = json.dumps(animal)
# print(as_json[0])
# test = "{'type': 'cat', 'age': 12}"
# print(test)

print("test")
test = json.loads("test")
print(test)

def analyzViewingHistory(shows, movies):
    try:
        grouped_titles_shows = shows['seriesTitle'].value_counts()
        num_movies = movies['videoTitle'].nunique()
        num_shows = shows['seriesTitle'].nunique()
        print("num_movies: " + num_movies)
        num_total = num_movies + num_shows
        duration_movies_min = int(movies['duration'].sum())/60
        duration_movies_str = str(datetime.timedelta(minutes=duration_movies_min))
        duration_shows_min = int(shows['duration'].sum())/60
        duration_shows_str = datetime.timedelta(minutes=duration_shows_min)
        print("duration_movies_min: " + duration_movies_min)
        totalTime_min = duration_movies_min + duration_shows_min
        totalTime_str = datetime.timedelta(minutes=totalTime_min)
        per_day_shows = shows.groupby(['day_of_week'], as_index=False).sum()
        per_day_shows['duration_s'] = per_day_shows['duration']
        per_day_shows = per_day_shows[['day_of_week', 'duration_s']]
        per_day_movies = movies.groupby(['day_of_week'], as_index=False).sum()
        per_day_movies['duration_m'] = per_day_movies['duration']
        per_day_movies = per_day_movies[['day_of_week', 'duration_m']]
        per_day = pd.merge(per_day_shows, per_day_movies, on='day_of_week', how='outer').fillna(0)
        per_day['duration_t'] = per_day['duration_s'] + per_day['duration_m']
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
            days[day] = float(per_day.loc[per_day['day_of_week']==day, 'duration_t']) if day in per_day.values else 0
    
        months = {
            "January":0,
            "February":0,
            "March":0,
            "April":0,
            "May":0,
            "June":0,
            "July":0,
            "August":0,
            "September":0,
            "October":0,
            "November":0,
            "December":0,
        }
        per_month_shows = shows.groupby(['month'], as_index=False).sum()
        per_month_shows['duration_s'] = per_month_shows['duration']
        per_month_shows = per_month_shows[['month', 'duration_s']]
        per_month_movies = movies.groupby(['month'], as_index=False).sum()
        per_month_movies['duration_m'] = per_month_movies['duration']
        per_month_movies = per_month_movies[['month', 'duration_m']]
        per_month = pd.merge(per_month_shows, per_month_movies, on='month', how='outer').fillna(0)
        per_month['duration_t'] = per_month['duration_s'] + per_month['duration_m']
        for month in months:
            months[month] = float(per_month.loc[per_month['month']==month, 'duration_t']) if month in per_month.values else 0
        shows = shows.replace(r'^\s*$', np.nan, regex=True)
        movies = movies.replace(r'^\s*$', np.nan, regex=True)
        return {
            "basic stats": {
                "watched_t": num_total,
                "watched_m": num_movies,
                "watched_s": num_shows,
                "time_spent_t": totalTime_min,
                "time_spent_m": duration_movies_min,
                "time_spent_s": duration_shows_min,
            },
            "days": days,
            "months": months
        }
    except:
        return "error"
    
