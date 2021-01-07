from bs4 import BeautifulSoup
import requests
import re


url = 'https://www.netflix.com/title/70195800'
urlContent = requests.get(url)
soup = BeautifulSoup(urlContent.text, 'html.parser')
soup = soup.find_all('section', {"id": "section-hero"})[0]
soup = soup.find_all('div', {"class": "hero-container"})[0]
soup = soup.find_all('div', {"class": "hero-image-container"})[0]
soup = soup.find_all('div', {"class": "hero-image hero-image-desktop"})[0]
soup = soup['style']

soupSplit = dict(item.split(":", 1) for item in soup.split(";"))
imageURL = soupSplit['background-image']
url = imageURL[len('url("'):-len('")')]
print(url)


  "browser_action": {
    "default_title": "Netflix Wrapped"
  },



  {
  "manifest_version": 2,
  "name": "Netflix Wrapped",
  "description": "Netflix Wrapped - your 2020 watch history summarized",
  "version": "1.5",
  "icons": { 
    "16": "files/icon16.png",
    "48": "files/icon48.png",
   "128": "files/icon128.png" 
  },
  "content_scripts": [
    {
      "matches": [
        "https://www.netflix.com/viewingactivity"
      ],
      "js": [
        "utils/utils.js",
        "utils/charts.js",
        "utils/data.js",
        "utils/loader.js",
        "utils/jquery.min.js"
      ],
      "css": [
      ],
      "run_at": "document_start"
    }
  ],
  "background": {
    "scripts": [
      "background.js"
    ],
    "persistent": true
  },
  "page_action": {
    "default_popup": "popup.html",
    "default_icon": { 
      "16": "files/icon16.png",
      "48": "files/icon48.png",
     "128": "files/icon128.png" 
    }
  },
  "web_accessible_resources": [
    "inject.js",
    "dashboard.html",
    "utils/utils.js",
    "utils/charts.js",
    "utils/data.js",
    "utils/loader.js",
    "utils/jquery.min.js"
  ],
  "permissions": [
    "https://*/*",
    "http://*/*",
    "tabs"
  ]
}