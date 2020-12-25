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
        console.log(data)
        redirectData(data);
    })
    .catch(function(error) {
      catch_error(error);
    });
};

function catch_error(error){
    // TODO:
    // Catch error, unable to display any data -> Prompt error message
    document.getElementById("main-display").innerHTML = `
        <br/> <br/>
        <h4> Error - Invalid data uploaded, please try again.</h4>
    `;
}


function redirectData(data){
    handleStatistics(data['statistics'])
    handleTitles(data['shows'], 'shows')
    handleTitles(data['movies'], 'movies')
}





// function get_data() {
//     // start_loader()
//     const URI = "http://127.0.0.1:5000"
//     const formData  = new FormData();
//     formData.append('timeFrame', "2020");
//     const requestOptions = {
//     method: 'POST',
//     body: formData,
//     };
//     fetch(`${URI}/get_data`, requestOptions)
//     .then(function(response) {
//       return response.json();
//     })
//     .then(function(data){
//         console.log(data)
//         // redirectData(data[0])
//     })
//     .catch(function(error) {
//       console.error(error)
//       catch_error(error)
//       });
// }

// function redirectData(stats){
//     for (const stat in stats["basics"]){
//         document.getElementById(stat).innerHTML = stats["basics"][stat];
//     }
//     // console.log(stats[0])
//     all_shows = ""
//     for(i = 0; i < stats['shows'].length; i++){
//         all_shows += `
//         <tr>
//             <td>${stats['shows'][i]['Date']}</td>
//             <td>${stats['shows'][i]['Title']}</td>
//             <td>${stats['shows'][i]['runtimeMinutes']}</td>
//         </tr>
//         `
//     }
//     // document.getElementById("all_shows").innerHTML = all_shows;


//     // for(const stat in stats){
//     //     console.log(stat)
//     // }

// }


// for (const stat in stats["basic stats"]){
//     document.getElementById(stat).innerHTML = stats["basic stats"][stat];
// }


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