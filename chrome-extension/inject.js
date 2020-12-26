(function () {


    URI = 'https://www.netflix.com/api/shakti';
    buildID = '/vb13b96d9';
    for (i = 1; i < 5; i++) {
        reqURI = `${URI}${buildID}/viewingactivity?pg=${i}&pgSize=20`;
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", reqURI, false);
        xmlHttp.send(null);
        console.log(JSON.parse(xmlHttp.responseText).viewedItems);
    }

    // just place a div at top right
    // var div = document.createElement('div');
    // div.style.position = 'fixed';
    // div.style.top = 0;
    // div.style.right = 0;
    // div.textContent = 'Injected!';
    // document.body.appendChild(div);

    alert('inserted self... giggity');

})();