from bs4 import BeautifulSoup
import requests
import re

url = 'https://www.netflix.com/ca/title/81227759'
urlContent = requests.get(url)
soup = BeautifulSoup(urlContent.text, 'html.parser')
soup = soup.find('section', { "id" : "section-hero"})
soup = soup.find('div', {"class" : "hero-container"})
soup = soup.find('div', {"class" : "hero-image-container"})
soup = soup.find('div', {"class" : "hero-image hero-image-desktop"})
soup = soup['style']

soupSplit = dict(item.split(":", 1) for item in soup.split(";"))
imageURL = soupSplit['background-image']
url = imageURL[len('url("'):-len('")')]
# 
print(url)