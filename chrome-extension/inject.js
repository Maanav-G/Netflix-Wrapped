const html = `
<div class="header">
<!-- <h1 class="display-6 container">Netflix Wrapped</h1> -->
<div class="container">
    <img src="./logo.svg" alt="" style="height: 125px">
</div>
</div>
<div class="container" id="main-display">
<br /><br />
<input type="file" id="fileUpload" />
<!-- <input type="file" id="file" className="form-control" onChange="get_data()" /> -->
<button onclick="test()">Test Fetch</button>
<br /> <br />
<h2 class="">
    Netflix Wrapped <br />
    <small><small><small><small>Jan 2020 - Dec 2020</small></small></small></small>
</h2>
<div class="break"></div>
<br />
<h4>Summary</h4>
<div class="break"></div>
<!-- FOLLOWING IS HARDCODED -->
<div class="row">
    <table class="table">
        <tbody>
            <tr>
                <td>Total Titles Watched</td>
                <td id="watched_t"></td>
            </tr>
            <tr>
                <td>Total Time Spent</td>
                <td id="time_spent_t">7 days, 13:34</td>
            </tr>
            <tr>
                <td>Total Shows Watched</td>
                <td id="watched_s"></td>
            </tr>
            <tr>
                <td>Total Time Spent Watching Shows</td>
                <td id="time_spent_s">7 days, 13:34</td>
            </tr>
        </tbody>
    </table>

</div>
<br /><br />
<div class="row">
    <div class="col">
        <h4>Top 10 Most Watched Shows:</h4>
        <div class="break"></div>
        <div id="top_10_shows">
            <table class="table">
                <tbody>
                    <tr>
                        <td>Friends</td>
                        <td>5 days, 12:22</td>
                        <td>702 Epi.</td>
                    </tr>
                    <tr>
                        <td>Modern Family </td>
                        <td>5 days, 12:22</td>
                        <td>233 Epi.</td>
                    </tr>
                    <tr>
                        <td>The Office (U.S.)</td>
                        <td>4 days, 12:22</td>
                        <td>192 Epi.</td>
                    </tr>
                    <tr>
                        <td>The Fosters </td>
                        <td>4 days, 12:22</td>
                        <td>182 Epi.</td>
                    </tr>
                    <tr>
                        <td>Naruto Shippuden</td>
                        <td>4 days, 12:22</td>
                        <td>159 Epi.</td>
                    </tr>
                    <tr>
                        <td>How to Get Away With Murder</td>
                        <td>3 days, 12:22</td>
                        <td>126 Epi.</td>
                    </tr>
                    <tr>
                        <td>Naruto</td>
                        <td>3 days, 12:22</td>
                        <td>122 Epi.</td>
                    </tr>
                    <tr>
                        <td>The Stranger </td>
                        <td>3 days, 12:22</td>
                        <td>78 Epi.</td>
                    </tr>
                    <tr>
                        <td>You</td>
                        <td>3 days, 12:22</td>
                        <td>22 Epi.</td>
                    </tr>
                    <tr>
                        <td>Imposters</td>
                        <td>1 day, 12:22</td>
                        <td>22 Epi.</td>
                    </tr>
                </tbody>
            </table>
        </div>

    </div>
    <div class="col">
        <h4>Top 10 Most Watched Movies:</h4>
        <div class="break"></div>
        <div id="top_10_movies">
            <table class="table">
                <tbody>
                    <tr>
                        <td>Friends</td>
                        <td>5 days, 12:22</td>
                        <td>702</td>
                    </tr>
                    <tr>
                        <td>Modern Family </td>
                        <td>5 days, 12:22</td>
                        <td>233</td>
                    </tr>
                    <tr>
                        <td>The Office (U.S.)</td>
                        <td>4 days, 12:22</td>
                        <td>192</td>
                    </tr>
                    <tr>
                        <td>The Fosters </td>
                        <td>4 days, 12:22</td>
                        <td>182</td>
                    </tr>
                    <tr>
                        <td>Naruto Shippuden</td>
                        <td>4 days, 12:22</td>
                        <td>159</td>
                    </tr>
                    <tr>
                        <td>How to Get Away With Murder</td>
                        <td>3 days, 12:22</td>
                        <td>126</td>
                    </tr>
                    <tr>
                        <td>Naruto</td>
                        <td>3 days, 12:22</td>
                        <td>122</td>
                    </tr>
                    <tr>
                        <td>The Stranger </td>
                        <td>3 days, 12:22</td>
                        <td>78</td>
                    </tr>
                    <tr>
                        <td>You</td>
                        <td>3 days, 12:22</td>
                        <td>22</td>
                    </tr>
                    <tr>
                        <td>Imposters</td>
                        <td>1 day, 12:22</td>
                        <td>22</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
<!-- ====================== -->

<!-- ====================== -->
<div class="row">
    <div class="col">
        <table class="table">
            <tbody id="all_shows">
            </tbody>
        </table>
    </div>
    <div class="col">
        <table class="table">
            <tbody id="all_movies">
            </tbody>
        </table>
    </div>
</div>
<!-- ====================== -->

</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js"
integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous">
</script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"
integrity="sha384-q2kxQ16AaE6UbzuKqyBE9/u/KzioAlnx2maXQHiDX9d4/zp8Ok3f+M7DPm+Ib6IU" crossorigin="anonymous">
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.min.js"
integrity="sha384-pQQkAEnwaBkjpqZ8RU1fF1AKtTcHJwFl3pblpTlHXybJjHpMYo79HY3hIi4NKxyj" crossorigin="anonymous">
</script>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript" src="main.js"></script>
`

var userData = new Array();
const YEAR = 2020;

(function () {
    // https://www.netflix.com/api/shakti/vb13b96d9/viewingactivity?pg=1&pgSize=100
    alert('Please wait a few moments');
    URI = 'https://www.netflix.com/api/shakti';
    buildID = '/vb13b96d9';

    var i = 0;
    var breakPoint = true;
    do {
        reqURI = `${URI}${buildID}/viewingactivity?pg=${i}&pgSize=100`;
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", reqURI, false);
        xmlHttp.send(null);
        userViewedItems = JSON.parse(xmlHttp.responseText).viewedItems;
        breakPoint = isRequired(userViewedItems);
        userData = [...userData, ...userViewedItems]
        i++;
    } while (i < 5); // TESTING - Replace with `breakPoint` 
    console.log(userData)
    handleUserData(userData);
})();


function handleUserData(event){
    const URI = "http://127.0.0.1:5000";
    const formData = new FormData();
    console.log(JSON.stringify(event))
    formData.append('userData', JSON.stringify(event));
    formData.append('timeFrame', "2020");
    const requestOptions = {
        method: 'POST',
        body: formData,
    };
    fetch(`${URI}/get_data`, requestOptions)
    .then(function(response) {
        console.log(response);
        return response.json();
    })
    .then(function(data){
        document.getElementById("appMountPoint").innerHTML = html
        // redirectData(data)
        // console.log(JSON.parse(data["movies"]));
        // console.log(JSON.parse(data["shows"]));
        // console.log(JSON.parse(data["top_shows"]));
        console.log(data);
    })
    .catch(function(error) {
        catch_error(error);
    });
};

function redirectData(data){
    try {
        handleStatistics(data['basic stats'])       
        handleTitles(parseCSV(data['shows']), 'all_shows')
        handleTitles(parseCSV(data['movies']), 'all_movies')
    } catch (error) {
        catch_error(error)
    }
}



function parseCSV(data){
    try {
        var obj = JSON.parse(data);
        return obj;
    } catch (error) {
        catch_error("Unable to JSONify");
    }
}


function isRequired(userViewedItems){
    const item = userViewedItems[userViewedItems.length - 1];
    const itemDate = new Date(item['date']);
    return itemDate.getFullYear() >= YEAR;
}

function catch_error(error){
    // TODO:
    // Catch error, unable to display any data -> Prompt error message
    document.getElementById("main-display").innerHTML = `
        <br/> <br/>
        <h4> Error - Invalid data uploaded, please try again.</h4>
    `;
}

