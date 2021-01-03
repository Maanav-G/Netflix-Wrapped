(function () {
    alert('Please wait a few moments');
    URI = 'https://www.netflix.com/api/shakti';
    const getBuildID = getNetflixBuildId();
    const buildID = getBuildID ? getBuildID : 'vb13b96d9';
    var userData = new Array();
    var i = 0;
    var breakPoint = true;
    do {
        reqURI = `${URI}/${buildID}/viewingactivity?pg=${i}&pgSize=100`;
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", reqURI, false);
        xmlHttp.send(null);
        userViewedItems = JSON.parse(xmlHttp.responseText).viewedItems;
        breakPoint = isRequired(userViewedItems);
        userData = [...userData, ...userViewedItems]
        i++;
        console.log(i + " - " + userViewedItems);
    } while (i<5); // Prod - Replace with `breakPoint` 
    handleUserData(userData);
})();

function handleUserData(event) {
    const requestOptions = {
        method: 'POST',
        body: JSON.stringify(event),
    };
    fetch("https://z27uo4gihl.execute-api.us-east-1.amazonaws.com/default/netflix-wrapped", requestOptions)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data)
            renderDashboard(data['analyzedData']);
        })
        .catch(function (error) {
            console.log(error);
        });
};


function handleUserDataLocal(event) {
    const URI = "http://127.0.0.1:5000";
    const formData = new FormData();
    formData.append('userData', JSON.stringify(event));
    formData.append('timeFrame', "2020");
    const requestOptions = {
        method: 'POST',
        body: formData,
    };
    fetch(`${URI}/get_data`, requestOptions)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data)
            renderDashboard(data);
        })
        .catch(function (error) {
            console.log(error);
        });
};

function renderDashboard(data){
    const template = '/dashboard.html'
    fetch(chrome.runtime.getURL(template))
        .then(response => response.text())
        .then(template => {
            console.log('injecting template');
            document.getElementsByClassName("bd")[0].innerHTML = template;
            injectElement("summarySection", summary(data['basic stats']));
            injectElement("topTenShows", topTenShows(
                sortDict(
                    parseCSV(data['top_shows'])
                )
            ));
            typeSplit(data['basic stats']);
            dayByDayChart(data['days']);
            monthlyChart(data['months']);
        })
        .catch(error => {
            catch_error("Could not load dashboard");
        });
}

function buildDashboard(data) {
    if (typeof variable !== 'undefined') catchError('undefined');
    try {
        document.getElementsByClassName("bd")[0].innerHTML = renderDashboard(data);
        typeSplit(data['basic stats']);
        dayByDayChart(data['days']);
        monthlyChart(data['months']);
    } catch (error) {
        catchError('undefined')
    }

}

function summary(data) {
    return `
    <h4>Summary</h4>
    <div class="break"></div>
    <table class="table" style="text-align: center">
        <thead>
            <tr>
                <th></th>
                <th># Watched</th>
                <th>Time Spent Watching</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Movies</td>
                <td id="time_spent_s">${data['watched_m']} movies</td>
                <td id="time_spent_s">${convertMinutes(data['time_spent_m'])}</td>
            </tr>
            <tr>
                <td>Series</td>
                <td id="time_spent_s">${data['watched_s']} shows</td>
                <td id="time_spent_s">${convertMinutes(data['time_spent_s'])}</td>
            </tr>
            <tr>
                <td>All Titles</td>
                <td id="time_spent_s">${data['watched_t']} titles</td>
                <td id="time_spent_s">${convertMinutes(data['time_spent_t'])}</td>
            </tr>
        </tbody>
    </table>
    `
}

function topTenShows(data) {
    var showlist = ""
    for (i = 0; i < Math.min(data.length, 10); i++) {
        template = `
        <tr>
            <td>${data[i][0]}</td>
            <td>${data[i][1]} episodes</td>
        </tr>
        `
        showlist = showlist + template;
    }
    // showlist = showlist + `
    //     * Viewing history only contains ${data.length} shows
    // `
    return showlist;
}

function showList(data) {
    var showlist = ""
    for (i = 0; i < 10; i++) {
        template = `
        <tr>
            <td>${data[i]['seriesTitle']}</td>
            <td>${data[i]['timeSpent']}</td>
            <td>${data[i]['numEpisodes']}</td>
        </tr>
        `
    }
}

function typeSplit(stats) {
    var ctx = document.getElementById('typeSplit').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Movies', 'Shows'],
            datasets: [{
                data: [stats['time_spent_m'], stats['time_spent_s']],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 1)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 0.2)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Movies vs Shows'
            },
            legend: {
                display: false,
            },
        }
    });

}

function dayByDayChart(weekdayData) {

    var ctx = document.getElementById('dayChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            datasets: [{
                data: [weekdayData['Monday'], weekdayData['Tuesday'], weekdayData['Wednesday'], weekdayData['Thursday'], weekdayData['Friday'], weekdayData['Saturday'], weekdayData['Sunday']],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Time Spent Watching per Day'
            },
            legend: {
                display: false,
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}
// months = {
//     "January","February","March","April","May","June","July","August","September","October","November","December"
// }
function monthlyChart(monthData) {
    var ctx = document.getElementById('monthChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            datasets: [{
                data: [monthData["January"], monthData["February"], monthData["March"], monthData["April"], monthData["May"], monthData["June"], monthData["July"], monthData["August"], monthData["September"], monthData["October"], monthData["November"], monthData["December"]],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Time Spent Watching per Montth'
            },
            legend: {
                display: false,
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}




