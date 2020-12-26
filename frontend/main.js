document.querySelector('#fileUpload').addEventListener('change', event => {
    handleFileUpload(event);
})

const handleFileUpload = event => {
    const URI = "http://127.0.0.1:5000";
    const userFile = event.target.files;
    const formData = new FormData();
    formData.append('file', userFile[0]);
    formData.append('timeFrame', "2020");
    const requestOptions = {
        method: 'POST',
        body: formData,
    };
    fetch(`${URI}/get_data`, requestOptions)
    .then(function(response) {
        return response.json();
    })
    .then(function(data){
        redirectData(data);
    })
    .catch(function(error) {
      catch_error(error);
    });
};

function test(){
    open('maanavgarg.com')
}

function scrapeViewingHistory(){
    URI = 'https://www.netflix.com/api/shakti';
    buildID = '/vb13b96d9';
    toReturn 
    for(i = 1; i < 5; i++) {
        reqURI = `${URI}${buildID}/viewingactivity?pg=${i}&pgSize=20`;
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", reqURI, false );
        xmlHttp.send( null );
        console.log(JSON.parse(xmlHttp.responseText).viewedItems);
    }
}



function catch_error(error){
    // TODO:
    // Catch error, unable to display any data -> Prompt error message
    document.getElementById("main-display").innerHTML = `
        <br/> <br/>
        <h4> Error - Invalid data uploaded, please try again.</h4>
    `;
}


function redirectData(data){
    try {
        handleStatistics(data['statistics'])       
        handleTitles(parseCSV(data['shows']), 'all_shows')
        handleTitles(parseCSV(data['movies']), 'all_movies')
    } catch (error) {
        catch_error(error)
    }
}


function handleStatistics(data){
    for (const stat in data){
        document.getElementById(stat).innerHTML = data[stat];
    }
}

function handleTitles(data, type){
    allTitles = ""
    for(i = 0; i < data.length; i++){
        allTitles += `
        <tr>
            <td>${data[i]['Date']}</td>
            <td>${data[i]['Title']}</td>
            <td>${data[i]['runtimeMinutes']}</td>
        </tr>
        `
    }
    document.getElementById(type).innerHTML = allTitles;
}

function parseCSV(data){
    try {
        var obj = JSON.parse(data);
        return obj;
    } catch (error) {
        catch_error(error);
    }
}



// // Load google charts
// google.charts.load('current', {
//     'packages': ['corechart']
// });
// google.charts.setOnLoadCallback(drawChart);

// // Draw the chart and set the chart values
// function drawChart() {
//     var data = google.visualization.arrayToDataTable([
//         ['Task', 'Hours per Day'],
//         ['Work', 8],
//         ['Friends', 2],
//         ['Eat', 2],
//         ['TV', 2],
//         ['Gym', 2],
//         ['Sleep', 8]
//     ]);

//     // Optional; add a title and set the width and height of the chart
//     var options = {
//         'title': 'My Average Day',
//         'width': 550,
//         'height': 400
//     };
//     // Display the chart inside the <div> element with id="piechart"
//     var chart = new google.visualization.PieChart(document.getElementById('piechart'));
//     chart.draw(data, options);
// }