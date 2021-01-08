# Netflix Wrapped

Netflix Wrapped - Your 2020 Netflix year in review, in the form of a Google Extension that fetches your viewing history and builds a concise dashboard with all your statistics. 

Feel free to download the “Netflix Wrapped” Google Extension from here and test it out yourself.

Where, this repo holds Google Extension component as well as the back-end portion of the ‘Netflix Wrapped’ extension.

## Google Extension

On one simple click, the Google Extension extracts your accounts full viewing history by querying Netflix’s hidden ‘Shakti’ API through the following request path: 

```
POST /api/shakti/${BuildID}/…
```
Where `${BuildID}` is simply just Shakti’s current build identifier, and at the time of this documentation it happens to be `vb13b96d9`

From here, since the user’s viewing history is fetched 20 `items` at a time, the extension then aggregates all the items and makes another post request to my flask backend on `…./getData`, which then fully analyzes the viewing history and returns back the user’s viewing statistics.  

## Flask Backend

## USED 
- ChartsJS
- Icons8
- Bootstrap 

##
- Num Episodes
- Time spent watching in one day 
- Save local data
- Save movie ID from 


[![](https://data.jsdelivr.com/v1/package/npm/chart.js/badge)](https://www.jsdelivr.com/package/npm/chart.js)