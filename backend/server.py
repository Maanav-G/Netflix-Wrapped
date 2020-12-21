from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import pandas as pd 

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/")
def index():
    return "Netflix Wrapped - Server"


@cross_origin(supports_credentials=True)
@app.route("/get_data", methods=['POST'])
def get_data():
    timeFrame = request.form['timeFrame']
    print(timeFrame)
    # curatedData = processViewingHistory(timeFrame)
    curated_data = [{
        "basic stats": {
            "watched_t": 60,
            "time_spent_t": 59,
        },
        "chart stats": {
            "chart 1":[1,2,3,4]
        },
        "raw data": {
            "chart 1":[1,2,3,4]
        }
    }]
    return jsonify(curated_data)

def processViewingHistory(timeFrame):
    start_date = timeFrame + "-01-01"
    end_date = timeFrame + "-12-31"
    # Netflix shows and movies dataset
    netflix_shows = pd.read_csv(r'./datasets/netflix_shows.csv') # 1969 rows
    netflix_movies = pd.read_csv(r'./datasets/netflix_movies.csv') # 4265 rows
    df = pd.read_csv(r'NetflixViewingHistory.csv')




if __name__ == '__main__':
    app.run(debug=True)

























