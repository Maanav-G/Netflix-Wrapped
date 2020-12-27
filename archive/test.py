import requests

# response = requests.request(method='GET', url="https://www.netflix.com/api/shakti/vb13b96d9/viewingactivity?pg=1&pgSize=20&guid=FZEVTV4IERDH5B3TXQLIWTJNLI&_=1608949865751&authURL=1608945627367.W4Op8o5ORUPyCwrRMfC3saITfK8%3D")
y = 'https://www.netflix.com/api/shakti/vb13b96d9/viewingactivity?pg=1&pgSize=20'
r = requests.request(url=y, method='GET')
print(r)