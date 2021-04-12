# Netflix Wrapped - Blog

This article covers why and how I went on about building my Netflix Wrapped Google Chrome extension - Which you can download here.

## Why I built this?

So honestly speaking, near the end of 2020 for a straight week, all I saw on my Instagram stories were my friends' Spotify Wrapped, that showed a bunch of statistics of their 2020 listening habits. Seeing this while being a proud Apple Music owner, I also wanted to sum up my 2020 year, and see some statistic on what I've been up too. Intially I thought on doing a Apple Music Wrapped, but that frankly felt too similar to Spotify, and plus I think I used Netflix way more during the pandemic than I did Apple Music - Thus was born the idea of Netflix Wrapped 2020.


## Phase 1: Webapp 

Before I the Google Chrome extension, I actually started this project off as a simple webapp where the user would upload their viewing history, and using which, my website would build them a dashboard full of their viewing statistics. However, after putting in countless dev hours this idea was eventual scraped. 

The main issue that arose was the lack of information that Netflix provided their user while exporting the viewing history. Outside of the Movie/TV Show Title and the Date Watched, no other information was given, and as you could imagine information such as the Title's ID and Duration are extremely crucial.

Additionally, when it came to TV Shows, the 'Title' field was consolidated, where instead of having a seperate field for the TV Show's main title and the episode title, we were given it as one field. 

After seeing these issues, I ended up spending countless hours trying to cross-reference and cross-build a main data set, using external data sets, that mapped the Netflix title to information we need (Genres, Actors, Ratings, Duration, etc.). However we quickly came across a large set of issues. For majority of my time, I was fiddling around with the main IMDB database.

- Duplicate Titles: Since we were querying databases using the actual title name, we ended finding more than one match. This would need to be replaced with some sort of ID, but again, Netflix didn't directly provide this information. 
- Multiple Durations: In the situation that we were able to match a Netflix title to a row in the IMDB database, sometimes the title would have multiple rows due to having multiple durations. This would occur when a TV Show would have of those one-off 'hour' long episodes, where the regular duration would be 20-25 min. 
- Average Duration: In external databases, all duration values for TV Shows were never exact, and only one average or approximate value was given. 

Seeing this, I quickly realized I had to start exploring different avenues, especially when it came to retrieving the user's viewing history.


## Shakti API

While trying to figure out different ways to extract the user's viewing history, the first thing I noticed is on the Viewing History page, the user can request 20 items at a time, and obviously there would need to be some sort of endpoint called in order to receive these from Netflix's back-end.   

Seeing this, I whipped open Chrome DevTools, opened up the requests panel, and noticed that the Viewing History page was requesting 20 items at a time from the Shakti API. I realized that the API was technically public to the user, however, could only be called from within a User's account. 

Once I started inspecting the data the API returned, I soon noticed that the Shakti API returned way more inofmration than Netflix chose to display. Other than the Title and Date, the API also provided us with the duration, type (Movie or TV Show) and title ID. 