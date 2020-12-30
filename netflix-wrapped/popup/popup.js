document.addEventListener('DOMContentLoaded', function() {
    var checkPageButton = document.getElementById('startExtension');
    checkPageButton.addEventListener('click', function() {
        console.log('ff')
    }, false);
  }, false);





// // listen for our browerAction to be clicked
// chrome.browserAction.onClicked.addListener(function (tab) {
// 	// for the current tab, inject the "inject.js" file & execute it
//     console.log('hyiß')
//     chrome.tabs.executeScript(tab.ib, {
// 		file: '../dashboard/dashboard.js'
// 	});
// });

// function test(){
//     console.log('ff')

// }
