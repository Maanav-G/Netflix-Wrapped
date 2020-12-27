var userData = new Array();
const YEAR = 2020;

(function () {
    // https://www.netflix.com/api/shakti/vb13b96d9/viewingactivity?pg=1&pgSize=100
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
    } while (i < 15); // TESTING - Replace with `breakPoint` 
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
        console.log(data);
    })
    .catch(function(error) {
        console.log('error');
    });
};


function isRequired(userViewedItems){
    const item = userViewedItems[userViewedItems.length - 1]
    const itemDate = new Date(item['date'])
    return itemDate.getFullYear() >= YEAR;
}
