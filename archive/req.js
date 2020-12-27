



xmlHttp.open( "GET", 'https://www.netflix.com/api/shakti/vb13b96d9/viewingactivity?pg=' + i + '&pgSize=20', false ); // false for synchronous request


URI = 'https://www.netflix.com/api/shakti'
buildID = '/vb13b96d9'
for(i = 0; i < 5; i++) {
    reqURI = `${URI}${buildID}/viewingactivity?pg=${i}&pgSize=20`
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", reqURI, false ); // false for synchronous request
    xmlHttp.send( null );
    console.log(JSON.parse(xmlHttp.responseText).viewedItems);
}


function scrapeViewingHistory(){
    URI = 'https://www.netflix.com/api/shakti'
    buildID = '/vb13b96d9'
    for(i = 0; i < 5; i++) {
        reqURI = `${URI}${buildID}/viewingactivity?pg=${i}&pgSize=20`
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", reqURI, false ); // false for synchronous request
        xmlHttp.send( null );
        console.log(JSON.parse(xmlHttp.responseText).viewedItems);
    }
}




chrome.tabs.create({ url: 'https://maanavgarg.com/' }, function(tab){
    chrome.tabs.sendMessage(tab.id, {greeting: "hello"}, function(){});
  });


    chrome.tabs.create({url: "https://www.stackoverflow.com", active: false }), tab =>{
        setTimeout(function(){
            chrome.tabs.remove(tab.id);
        },INTERVAL);
    }); 
