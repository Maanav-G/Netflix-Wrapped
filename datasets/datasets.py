import pandas as pd 
import numpy as np 

# netflix_df = pd.read_csv('netflix_titles.csv') # 6234 rows
# # Split dataset between shows and movies 
# netflix_shows = netflix_df[netflix_df['type']=='TV Show'] # 1969 rows
# netflix_movies = netflix_df[netflix_df['type']=='Movie'] # 4265 rows

# IMDB TV Show run time
basics = pd.read_csv(r'IMDB_tv_runtime.tsv', sep='\t', header=0)
basics = basics[basics['titleType'].isin(['tvSeries'])]
basics = basics[['originalTitle', 'runtimeMinutes']]
basics = basics[basics['runtimeMinutes'] != r"\N"]
basics = basics[basics['originalTitle'] != r"\N"]
basics = basics.groupby('originalTitle')['runtimeMinutes'].apply(list)
basics.to_csv('runtime.csv', sep='\t')
test = basics[basics['originalTitle'] == "Suits"]
print(test)

# netflix_shows_rt = pd.join(
#     [netflix_shows.set_index('title'),basics.set_index('primaryTitle')],
#     axis=1, 
#     join='inner'
# )

# for col in netflix_shows.columns:
#     print(col) 
#     print(netflix_shows.head()[col])
#     print(" ")
