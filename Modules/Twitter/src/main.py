import json
import base64
import io
from Tweet import Tweet
from httplib import *

CONSUMER_KEY = None
PRIVATE_KEY = None
BEARER_TOKEN = None
base_URL = "api.twitter.com"
tweets = []
connection = HTTPSConnection(base_URL)


def get_token():
    bearer_creds = base64.b64encode(CONSUMER_KEY + ":" + PRIVATE_KEY)
    headers = {"Authorization": "Basic " + bearer_creds,
               "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    body = "grant_type=client_credentials"
    connection.request("POST", "/oauth2/token", body, headers)
    response = connection.getresponse()
    if response.status == 200:
        ans = response.read()
        parsed = json.loads(ans)
        global BEARER_TOKEN
        BEARER_TOKEN = parsed["access_token"]
    else:
        print("Failed to authenticate")
        print(response.read())


def serialize_data():
    with io.open('../data/data.json', 'w') as f:
        json_file = {'CONSUMER_KEY': CONSUMER_KEY, 'PRIVATE_KEY': PRIVATE_KEY, 'BEARER_TOKEN': BEARER_TOKEN}
        f.write(unicode(json.dumps(json_file, ensure_ascii=False)))


def deserialize_data():
    with io.open('../data/data.json', 'r') as f:
        parsed = json.loads(f.readline())
        global CONSUMER_KEY
        global PRIVATE_KEY
        global BEARER_TOKEN
        CONSUMER_KEY = parsed["CONSUMER_KEY"]
        PRIVATE_KEY = parsed["PRIVATE_KEY"]
        try:
            BEARER_TOKEN = parsed["BEARER_TOKEN"]
        except Exception:
            get_token()


def tweets_marca_modelo(marca, modelo):
    query = "/1.1/search/tweets.json?q=%40{0}%20{1}%20since%3A2012-01-01&lang=en&count=50".format(marca, modelo)
    headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    connection.request("GET", url=query, headers=headers)
    response = connection.getresponse()
    if response.status == 200:
        ans = response.read()
        parsed = json.loads(ans)
        parse_tweets(parsed)
    else:
        print("Failed to search tweets")
        print(response.read())


def parse_tweets(parsed):
    for t in parsed["statuses"]:
        tweet = Tweet(t["id"], t["text"], "Positive")
        tweets.append(tweet)


deserialize_data()
tweets_marca_modelo('audi', 'a8')