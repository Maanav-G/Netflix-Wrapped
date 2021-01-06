const YEAR = 2020;

const injectElement = (elementId, data) => document.getElementById(elementId).innerHTML = data;

function getNetflixBuildId() {
    const scripts = Array.prototype.slice.call(document.scripts);
    let buildId = null;
    scripts.forEach((script, index) => {
        const buildIdIndex = script.innerHTML.indexOf('BUILD_IDENTIFIER');
        if (buildIdIndex > -1) {
            const text = script.innerHTML.substring(buildIdIndex + 19);
            buildId = text.substring(0, text.indexOf('"'));
        }
    });
    return buildId;
}

function convertMinutes(num) {
    d = Math.floor(num / 1440); // 60*24
    h = Math.floor((num - (d * 1440)) / 60);
    m = Math.round(num % 60);

    if (d > 0) {
        return (d + " days, " + h + " hours, " + m + " minutes");
    } else if (h > 0) {
        return (h + " hours, " + m + " minutes");
    } else {
        return (m + " minutes");
    }
}


function sortDict(dict) {
    var items = Object.keys(dict).map(function (key) {
        return [key, dict[key]];
    });
    items.sort(function (first, second) {
        return second[1] - first[1];
    });
    return items;
}

function parseCSV(data) {
    try {
        var obj = JSON.parse(data);
        return obj;
    } catch (error) {
        catchError("Unable to JSONify");
    }
}


function isRequired(userViewedItems) {
    const item = userViewedItems[userViewedItems.length - 1];
    const itemDate = new Date(item['date']);
    return itemDate.getFullYear() >= YEAR;
}

function catchError(error) {
    // TODO:
    // Catch error, unable to display any data -> Prompt error message
    document.getElementsByClassName("bd")[0].innerHTML = `
        <br/> <br/>
        <h4> Error - ${error}</h4>
    `;
}

