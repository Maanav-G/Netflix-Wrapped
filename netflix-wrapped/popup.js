document.getElementById('start').addEventListener('click', startWrapped);


function startWrapped() {
  chrome.tabs.executeScript({
    file: 'inject.js'
  });
}
// function startWrapped() {
//   if(location.host == "www.netflix.com" && location.pathname == "/viewingactivity")
// }

