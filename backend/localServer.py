from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import pandas as pd 
import datetime
import numpy as np
import json

# 
from bs4 import BeautifulSoup
import requests
import re


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
def index():
    return "Netflix Wrapped - Server"

@cross_origin(supports_credentials=True)
@app.route("/get_data", methods=['POST'])
def get_data():
    timeFrame = request.form['timeFrame']
    print(request.form['userData'])
    print(json.loads(request.form['userData']))
    userViewingHistory = pd.DataFrame(json.loads(request.form['userData']))
    curate = curateData(userViewingHistory, timeFrame)    
    return curate
        
def curateData(userData, timeFrame):
    userViewingHistory = processViewingHistory(userData, timeFrame)[0]
    analyzedData = analyzeViewingHistory(
        userViewingHistory['shows'], 
        userViewingHistory['movies']
        )
    return analyzedData


def processViewingHistory(userData, timeFrame):
    # Date range spanning 2020
    start_date = timeFrame + "-01-01"
    end_date = timeFrame + "-12-31"
    # User's viewing history
    df = userData
    # Get watch history for specified year
        # dates = df[df.dateStr >= start_date]
        # df = dates[dates.dateStr <= end_date]
    # Devise new column for day of week
    df['DateTime'] = pd.to_datetime(df['dateStr'], errors='coerce')
    df['Year'] = df['DateTime'].dt.year
    df = df[df["Year"]==2020]
    
    df['day_of_week'] = df['DateTime'].dt.day_name() # df['day_of_week'] = df['DateTime'].dt.weekday
    df['month'] = df['DateTime'].dt.month_name() # df['day_of_week'] = df['DateTime'].dt.month
    # Split between TV shows and movies based on a lack of series
    # TODO - Find a more robust way to split dataset... 
    shows = df[df['series'].notna()]
    movies = df[df['series'].isna()]

    return [{
        'shows': shows,
        'movies': movies
    }]


def analyzeViewingHistory(shows, movies):
    # Total Unique Titles
    # grouped_titles_movies = movies['videoTitle'].sum()
    # grouped_titles_shows_ = shows['seriesTitle'].sum()
    # print(grouped_titles_shows_)
    grouped_titles_shows = shows.groupby('seriesTitle')['series'].value_counts().reset_index(name='count').sort_values(by=['count'], ascending=False)
    grouped_titles_shows['url'] = grouped_titles_shows.apply(lambda row: getImageURL(int(row["series"])), axis=1)
    print(grouped_titles_shows)
    # print(grouped_titles_shows.to_json())
    # grouped_total = grouped_titles_movies + grouped_titles_shows 
    # Num Movies
    num_movies = movies['videoTitle'].nunique()
    # Num Shows
    num_shows = shows['seriesTitle'].nunique()
    # Total Titles
    num_total = num_movies + num_shows
    # Movies Duration
    duration_movies_min = int(movies['duration'].sum())/60
    duration_movies_str = str(datetime.timedelta(minutes=duration_movies_min))
    # Shows Duration
    duration_shows_min = int(shows['duration'].sum())/60
    duration_shows_str = datetime.timedelta(minutes=duration_shows_min)
    # Total Time
    totalTime_min = duration_movies_min + duration_shows_min
    totalTime_str = datetime.timedelta(minutes=totalTime_min)
    # Day-by-Day
    per_day_shows = shows.groupby(['day_of_week'], as_index=False).sum()
    # print("per_day_shows: " + per_day_shows)coffe
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
        "months": months,
        "top_shows": grouped_titles_shows.to_json(orient = 'records'),
        "shows": shows.to_json(orient = 'records'),
        "movies": movies.to_json(orient = 'records'),
    }


def getImageURL(id):
    url = "https://www.netflix.com/ca/title/" + str(id)
    try:
        urlContent = requests.get(url)
        soup = BeautifulSoup(urlContent.text, 'html.parser')
        soup = soup.find('section', { "id" : "section-hero"})
        soup = soup.find('div', {"class" : "hero-container"})
        soup = soup.find('div', {"class" : "hero-image-container"})
        soup = soup.find('div', {"class" : "hero-image hero-image-desktop"})
        soup = soup['style']
        soupSplit = dict(item.split(":", 1) for item in soup.split(";"))
        imageURL = soupSplit['background-image']
        url = imageURL[len('url("'):-len('")')]
    except:
        url = "#"
    return url


if __name__ == '__main__':
    app.run(debug=True)

























