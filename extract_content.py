#

import logging

import pymongo
import pytz


def extract_text(article_url):
    import requests
    import json
    headers = {
        'Content-Type': "text/html"
    }

    url = "https://api.diffbot.com/v3/analyze"

    querystring = {"token": "dcb988ea1d7aba4107ac9d16e3a3c311", "url": article_url}
    response = requests.request("GET", url, headers=headers, params=querystring)

    d = response.json()
    return d


db = pymongo.MongoClient(host='192.168.31.92', port=27017)  # , 'chatbot_htkh_misa-meinvoice-web', 'history'
db = db['resultdb']
col = db['cafef']

for v in col.find({"text": {"$exists": False}}):
    url = v['url']
    print(url)
    response = extract_text(url)
    if response['objects']:
        text = response['objects'][0]['text']
        v['text'] = text
        col.save(v)
