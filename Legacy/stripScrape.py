# Generates scrapes of every garfield strip
# File may need some repair to scrape future strips, as start/end dates are hardcoded

import re
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
site = 'http://pt.jikos.cz/garfield'
yearstart = 1978
yearend = 2019
startindex = 6
endindex = 4
excludeMarkers = ["valid","vim"]
i = yearstart
t = startindex
collecting = []
def checkContaining(checkedString,checkArray):
    metric = False
    for keyWord in checkArray:
        metric |= (keyWord in checkedString)
    return metric
for i in tqdm(range(yearstart,yearend)):
    for t in range(1,13):
        url = site + "/" + str(i) + "/" + str(t) + "/"
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        urls = [img['src'] for img in img_tags]


        for url in urls:
            print(url)
            filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url).group(1)
            if 'http' not in url:
                url = '{}{}'.format(site, url)
            if not checkContaining(filename,excludeMarkers):
                collecting.append((filename,url))
json.dump({"URLs":collecting,"SetName":"Strips"},open("../Data/jmappers/stripurlfile.json","w"))