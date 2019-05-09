# Generates scrapes from the top of /r/imsorryjon
# Requires redditdetails.private JSON in order to work properly

import praw
import requests
import pandas as pd
import datetime as dt
import os
import json
import re
from tqdm import tqdm
pattern = r'jpeg|jpg|png'

privatedata = json.load(open("redditdetails.private","r"))
reddit = praw.Reddit(client_id=privatedata["client_id"],
                     client_secret=privatedata["client_secret"],
                     user_agent=privatedata["user_agent"],
                     username=privatedata["username"],
                     password=privatedata["password"])
subreddit = reddit.subreddit('imsorryjon')
top_subreddit = subreddit.top(limit = 10000)
collection = []
for sub in tqdm(top_subreddit):
    try:
        url = sub.url
        match = re.search(pattern, url)
        if match:
            filename = url.split('/')[-1]
            collection.append((filename,str(url)))
    except Exception as e:
        print(e)
json.dump({"URLs": collection,"SetName":"ImSorryJon"},open("../Data/jmappers/sorryurlfile.json","w"))