import pandas as pd 
import numpy as np 

# IMDB TV Show run time
basics = pd.read_csv(r'IMDB_tv_runtime.tsv', sep='\t', header=0)
basics = basics[basics['titleType'].isin(['tvSeries', 'tvMiniSeries', 'movie'])]
basics['titleType'] = basics['titleType'].replace(['tvSeries', 'tvMiniSeries'], ['show', 'show'])
basics = basics[basics['runtimeMinutes'] != r"\N"]
basics = basics[basics['originalTitle'] != r"\N"]
basics['runtimeMinutes'] = pd.to_numeric(basics['runtimeMinutes'])
# basics = basics.groupby('originalTitle')['runtimeMinutes'].mean()
basics = basics.rename(columns={"originalTitle": "title"})
basics_tv = basics[basics['titleType'].isin(['show'])]
basics_movie = basics[basics['titleType'].isin(['movie'])]
basics_tv.to_csv('imdb_show.csv', sep=',')
basics_movie.to_csv('imdb_movies.csv', sep=',')
