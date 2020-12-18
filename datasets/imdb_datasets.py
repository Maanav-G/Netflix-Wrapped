import pandas as pd 
import numpy as np 

# IMDB TV Show run time
basics = pd.read_csv(r'IMDB_tv_runtime.tsv', sep='\t', header=0)
basics = basics[basics['titleType'].isin(['tvSeries', 'tvMiniSeries'])]
basics = basics[['originalTitle', 'runtimeMinutes']]
basics = basics[basics['runtimeMinutes'] != r"\N"]
basics = basics[basics['originalTitle'] != r"\N"]
basics['runtimeMinutes'] = pd.to_numeric(basics['runtimeMinutes'])
basics = basics.groupby('originalTitle')['runtimeMinutes'].mean()
basics.to_csv('runtime.csv', sep=',')


# for col in netflix_shows.columns:
#     print(col) 
#     print(netflix_shows.head()[col])
#     print(" ")
