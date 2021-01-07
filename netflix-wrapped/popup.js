function hello() {
    chrome.tabs.executeScript({
      file: 'inject.js'
    }); 
  }
  
  document.getElementById('start').addEventListener('click', hello);