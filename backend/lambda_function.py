import json
import pandas as pd 
import datetime


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        bodyValid = 'true'
    except:
        body = "error"
        bodyValid = 'false'

    try:
        userViewingHistory = pd.DataFrame(body)
        dataframe = userViewingHistory.to_json(orient = 'records')
        dfValid = "true"
    except:
        userViewingHistory = "error"
        dataframe = body
        dfValid = "false"
        
    try:
        curate = curateData(userViewingHistory)
    except:
        curate = "err"
    
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Methods": "POST"
        },
        'body': json.dumps({
            'all_titles': body,
            'analyzedData': curate
        })
    }
    
def curateData(userData):
    try:
        userViewingHistory = processViewingHistory(userData)[0]
    except:
        userViewingHistory = 'error'
    analyzedData = analyzeViewingHistory(
        userViewingHistory['shows'], 
        userViewingHistory['movies'],
        userViewingHistory['allTitles']
        )
    return analyzedData

def processViewingHistory(userData):
    df = userData
    df['DateTime'] = pd.to_datetime(df['dateStr'], errors='coerce')
    df['Year'] = df['DateTime'].dt.year
    df = df[df["Year"]==2020]
    df['day_of_week'] = df['DateTime'].dt.day_name()
    df['month'] = df['DateTime'].dt.month_name()
    shows = df[df['series'].notna()]
    movies = df[df['series'].isna()]
    return [{
        'shows': shows,
        'movies': movies,
        'allTitles': df
    }]
    
def analyzeViewingHistory(shows, movies, allTitles):
    try:
        try:
            grouped_titles_shows = shows.groupby('seriesTitle')['series'].value_counts().reset_index(name='count').sort_values(by=['count'], ascending=False)
            grouped_titles_shows = grouped_titles_shows.to_json(orient = 'records')
        except:
            grouped_titles_shows = "err"
        num_movies = movies['videoTitle'].nunique()
        num_shows = shows['seriesTitle'].nunique()
        num_total = num_movies + num_shows
        duration_movies_min = int(movies['duration'].sum())/60
        duration_shows_min = int(shows['duration'].sum())/60
        totalTime_min = duration_movies_min + duration_shows_min
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
        per_month_shows = shows.groupby(['month'], as_index=False).sum()
        per_month_shows['duration_s'] = per_month_shows['duration']
        per_month_shows = per_month_shows[['month', 'duration_s']]
        per_month_movies = movies.groupby(['month'], as_index=False).sum()
        per_month_movies['duration_m'] = per_month_movies['duration']
        per_month_movies = per_month_movies[['month', 'duration_m']]
        per_month = pd.merge(per_month_shows, per_month_movies, on='month', how='outer').fillna(0)
        per_month['duration_t'] = per_month['duration_s'] + per_month['duration_m']
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
        for month in months:
            months[month] = float(per_month.loc[per_month['month']==month, 'duration_t']) if month in per_month.values else 0
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
            "months": months,
            "top_shows": grouped_titles_shows,
            "shows": shows.to_json(orient = 'records'),
            "movies": movies.to_json(orient = 'records'),
            "allTitles": allTitles.to_json(orient = 'records')
        }
    except:
        return "error"
    
