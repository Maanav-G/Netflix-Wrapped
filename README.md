# Netflix Wrapped

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


##
- Num Episodes
