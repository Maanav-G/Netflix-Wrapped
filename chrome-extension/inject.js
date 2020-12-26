var userData = new Array();
const YEAR = 2020;

(function () {
    
    alert('Please wait a few moments');
    URI = 'https://www.netflix.com/api/shakti';
    buildID = '/vb13b96d9';

    var i = 1;
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
    } while (i < 6); // TESTING - Replace with `breakPoint` 
    console.log(userData)




})();


function isRequired(userViewedItems){
    const item = userViewedItems[userViewedItems.length - 1]
    console.log(item)
    const itemDate = new Date(item['date'])
    return itemDate.getFullYear() >= YEAR;
}

// for (i = 1; i < 5; i++) {
//     reqURI = `${URI}${buildID}/viewingactivity?pg=${i}&pgSize=20`;
//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.open("GET", reqURI, false);
//     xmlHttp.send(null);
//     userViewedItems = JSON.parse(xmlHttp.responseText).viewedItems
//     if(!Array.isArray(userViewedItems) || !userViewedItems.length){
//         break;
//     }
//     appendData(JSON.parse(xmlHttp.responseText).viewedItems)
// }

// var i = 0;
// while (true) {
//     reqURI = `${URI}${buildID}/viewingactivity?pg=${i}&pgSize=100`;
//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.open("GET", reqURI, false);
//     xmlHttp.send(null);
//     userViewedItems = JSON.parse(xmlHttp.responseText).viewedItems;
//     if(!Array.isArray(userViewedItems) || !userViewedItems.length){
//         break;
//     }
//     console.log(userViewedItems)
//     appendData(userViewedItems)
//     i++;
// }

    // document.getElementsByClassName("bd")[0].innerHTML = dashboard;
