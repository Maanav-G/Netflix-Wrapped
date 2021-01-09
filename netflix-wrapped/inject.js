(function () {
    insertMetaTag();
    startLoader();
    setTimeout(() => {
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
        } while (breakPoint); // Prod - Replace with `breakPoint` 
        handleUserData(userData);
    }, 500);

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
            renderDashboard(data['analyzedData'], data['analyzedData']['allTitles']);
        })
        .catch(function (error) {
            catchError('Data could not be fetched');
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
            renderDashboard(data);
        })
        .catch(function (error) {
            console.log(error);
        });
};

function renderDashboard(data, titles) {
    const template = '/dashboard.html'
    fetch(chrome.runtime.getURL(template))
        .then(response => response.text())
        .then(template => {
            document.getElementsByClassName("bd")[0].innerHTML = template;
            injectElement("summarySection", summary(data['basic stats']));
            injectElement("topTenShows", topTenShows(
                JSON.parse(data['top_shows'])
            ));
            injectElement("all_titles", allTitles(
                JSON.parse(titles)
            ));
            injectElement("date", calcDate(
                JSON.parse(titles)
            ));
            typeSplit(data['basic stats']);
            dayByDayChart(data['days']);
            monthlyChart(data['months']);
        })
        .catch(error => {
            catchError("Could not load dashboard");
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
    <tr>
        <td><img src="https://img.icons8.com/ios-filled/40/000000/movie-projector.png"/></td>
        <td>Movies</td>
        <td id="time_spent_s">${data['watched_m']} movies</td>
        <td id="time_spent_s">${convertMinutes(data['time_spent_m'])}</td>
    </tr>
    <tr>
        <td><img src="https://img.icons8.com/android/40/000000/retro-tv.png"/></td>
        <td>Series</td>
        <td id="time_spent_s">${data['watched_s']} shows</td>
        <td id="time_spent_s">${convertMinutes(data['time_spent_s'])}</td>
    </tr>
    <tr>
        <td></td>
        <td>All Titles</td>
        <td id="time_spent_s">${data['watched_t']} titles</td>
        <td id="time_spent_s">${convertMinutes(data['time_spent_t'])}</td>
    </tr>
    `;
}

function topTenShows(data) {
    var showlist = "";
    for (i = 0; i < Math.min(data.length, 10); i++) {
        template = `
        <tr>
            <td>
                <a href="https://www.netflix.com/title/${data[i]['series']}" target="_blank">
                    ${data[i]['seriesTitle']}
                </a>
            </td>
            <td>${data[i]['count']} episodes</td>
        </tr>
        `;
        showlist += template;
    }
    if (data.length < 10) {
        showlist = showlist + `
            <br/>
            * Viewing history only contains ${data.length} shows
        `
    }
    return showlist;
}

function allTitles(data) {
    var showList = "";
    for (i = 0; i < data.length; i++) {

        template = `
        <tr>
            <td>
                ${
                    (data[i]['seriesTitle'] == undefined) ? `<img src="https://img.icons8.com/ios-filled/40/000000/movie-projector.png"/>` : `<img src="https://img.icons8.com/android/40/000000/retro-tv.png"/>`
                }
            </td>
            <td>${data[i]['dateStr']}</td>
            <td>
                <a href="https://www.netflix.com/title/${data[i]['movieID']}" target="_blank" >
                    ${
                        (data[i]['seriesTitle'] == undefined) ? "" : (data[i]['seriesTitle'] + " -")
                    } ${data[i]['title']} 
                </a>
            </td>
            <td>
                ${
                    new Date(data[i]['duration'] * 1000).toISOString().substr(11, 8)
                }
            </td>
        </tr>
        `;
        showList += template;
    }
    return showList;
}

function calcDate(titles) {
    const earliestTitle = titles[titles.length - 1]
    const lastTitle = titles[0]
    return (
        earliestTitle['dateStr'] + " to " + lastTitle['dateStr']
    )
}

function secondsToHms(d) {
    d = Number(d);
    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);
    var s = Math.floor(d % 3600 % 60);
    return ('0' + h).slice(-2) + ":" + ('0' + m).slice(-2) + ":" + ('0' + s).slice(-2);
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
    const total = stats['time_spent_m'] + stats['time_spent_s']
    var ctx = document.getElementById('typeSplit').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Movies', 'Shows'],
            datasets: [{
                data: [
                    stats['time_spent_m'] / total,
                    stats['time_spent_s'] / total
                ],
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
                data: [weekdayData['Monday'] / 60, weekdayData['Tuesday'] / 60, weekdayData['Wednesday'] / 60, weekdayData['Thursday'] / 60, weekdayData['Friday'] / 60, weekdayData['Saturday'] / 60, weekdayData['Sunday'] / 60],
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
                data: [monthData["January"] / 60, monthData["February"] / 60, monthData["March"] / 60, monthData["April"] / 60, monthData["May"] / 60, monthData["June"] / 60, monthData["July"] / 60, monthData["August"] / 60, monthData["September"] / 60, monthData["October"] / 60, monthData["November"] / 60, monthData["December"] / 60],
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
                    'rgba(255, 99, 132, 0.2)'
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
                text: 'Time Spent Watching per Month'
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