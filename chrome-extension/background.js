// document.addEventListener('DOMContentLoaded', function () {
//     var checkPageButton = document.getElementById('button');
//     checkPageButton.addEventListener('click', function () {

//         chrome.tabs.getSelected(null, function (tab) {
//             pullData()
//             // d = document;

//             // var f = d.createElement('form');
//             // f.action = 'http://gtmetrix.com/analyze.html?bm';
//             // f.method = 'post';
//             // var i = d.createElement('input');
//             // i.type = 'hidden';
//             // i.name = 'url';
//             // i.value = tab.url;
//             // f.appendChild(i);
//             // d.body.appendChild(f);
//             // f.submit();
//         });
//     }, false);
// }, false);



// function pullData() {
//     open('ma')
//     URI = 'https://www.netflix.com/api/shakti';
//     buildID = '/vb13b96d9';
//     for (i = 1; i < 5; i++) {
//         reqURI = `${URI}${buildID}/viewingactivity?pg=${i}&pgSize=20`;
//         var xmlHttp = new XMLHttpRequest();
//         xmlHttp.open("GET", reqURI, false);
//         xmlHttp.send(null);
//         console.log(JSON.parse(xmlHttp.responseText).viewedItems);
//     }
// }

// listen for our browerAction to be clicked
chrome.browserAction.onClicked.addListener(function (tab) {
	// for the current tab, inject the "inject.js" file & execute it
	chrome.tabs.executeScript(tab.ib, {
		file: 'inject.js'
	});
});