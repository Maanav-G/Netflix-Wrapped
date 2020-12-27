
    # # Split between TV shows and movies based on title 
    # df['Shows'] = df['Title'].str.split(':',2)
    # df['len'] = df['Shows'].str.len()
    # shows = df[df['len'] == 3]
    # movies = df[df['len'] != 3]
    # # Build new columns for Shows - Title, Season, Episode
    # shows = shows.join(shows['Title'].str.split(':', 2, expand=True).rename(columns={0:'title', 1:'season', 2:'episode'}))
    # movies['title'] = movies['Title']
    # # Add runtime for shows
    # shows_rt = pd.merge(shows, netflix_shows, on='title', how='left')
    # shows_rt = shows_rt.fillna(22)
    # # Add runtime for movies
    # movies_rt = pd.merge(movies, netflix_movies, on='title', how='left')