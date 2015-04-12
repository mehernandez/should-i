import json
import base64
import urllib
import io
from Tweet import Tweet
from TweetList import TweetList
from httplib import *
from Models.Modulo import *


class Twitter(Modulo):

    CONSUMER_KEY = None
    PRIVATE_KEY = None
    BEARER_TOKEN = None
    MASHAPE_TOKEN = None
    base_URL = "api.twitter.com"
    connection = HTTPSConnection(base_URL)

    def __init__(self, path):
        with io.open(path, 'r') as f:
            parsed = json.loads(f.readline())
            global CONSUMER_KEY
            global PRIVATE_KEY
            global BEARER_TOKEN
            global MASHAPE_TOKEN
            CONSUMER_KEY = parsed["CONSUMER_KEY"]
            PRIVATE_KEY = parsed["PRIVATE_KEY"]
            MASHAPE_TOKEN = parsed["MASHAPE_TOKEN"]
            try:
                BEARER_TOKEN = parsed["BEARER_TOKEN"]
            except Exception:
                BEARER_TOKEN = self.get_token()

    @staticmethod
    def serialize_data():
        with io.open('../data/data.json', 'w') as f:
            json_file = {'CONSUMER_KEY': CONSUMER_KEY,
                         'PRIVATE_KEY': PRIVATE_KEY,
                         'BEARER_TOKEN': BEARER_TOKEN,
                         'MASHAPE_TOKEN': MASHAPE_TOKEN}
            f.write(unicode(json.dumps(json_file, ensure_ascii=False)))

    def get_token(self):
        bearer_creds = base64.b64encode(CONSUMER_KEY + ":" + PRIVATE_KEY)
        headers = {"Authorization": "Basic " + bearer_creds,
                   "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        body = "grant_type=client_credentials"
        self.connection.request("POST", "/oauth2/token", body, headers)
        response = self.connection.getresponse()
        if response.status == 200:
            ans = response.read()
            parsed = json.loads(ans)
            return parsed["access_token"]
        else:
            print("Failed to authenticate")
            print(response.read())

    def pedido(self, perfil=None, tiempo=-1, params=None):
        return self.tweets_marca_modelo(params["marca"] + " " + params["modelo"])

    def tweets_marca_modelo(self, contenido):
        tweets = TweetList()
        query = "{0} since:2013-01-01".format(contenido)
        query = "/1.1/search/tweets.json?q=" + urllib.quote(query.encode('utf8')) + "&lang=en&include_entities=false"
        print query
        headers = {"Authorization": "Bearer " + BEARER_TOKEN}
        self.connection.request("GET", url=query, headers=headers)
        response = self.connection.getresponse()
        if response.status == 200:
            ans = response.read()
            parsed = json.loads(ans)
            tweets = self.parse_tweets(parsed)
            return tweets
        else:
            print("Failed to search tweets")
            print(response.read())
            return tweets

    def parse_tweets(self, parsed):
        tweets = []
        for t in parsed["statuses"]:
            tweet = Tweet(t["id"], t["text"], t["user"]["screen_name"], t["created_at"])
            self.set_oembed(tweet)
            self.set_mood_for_tweet(tweet)
            tweets.append(tweet)

        return tweets

    @staticmethod
    def set_mood_for_tweet(tweet):
        sentiment_connection = HTTPSConnection('twinword-sentiment-analysis.p.mashape.com')
        headers = {"X-Mashape-Key": "{0}".format(MASHAPE_TOKEN),
                   "Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "application/json"}
        body = "text={0}".format(tweet.text.encode('utf-8'))
        sentiment_connection.request("POST", "/analyze/", body, headers)
        response = sentiment_connection.getresponse()
        if response.status == 200:
            ans = response.read()
            parsed = json.loads(ans)
            tweet.mood = parsed["type"]
            tweet.score = parsed["score"]
        else:
            print("Failed to get mood")
            print(response.read())

    def set_oembed(self, tweet):
        headers = {"Authorization": "Bearer " + BEARER_TOKEN}
        self.connection.request("GET", url="/1.1/statuses/oembed.json?id={0}".format(tweet.identifier), headers=headers)
        response = self.connection.getresponse()
        if response.status == 200:
            ans = response.read()
            parsed = json.loads(ans)
            tweet.html = parsed["html"]
        else:
            print("Failed to get oembed tweets")
            print(response.read())

twitter = Twitter('../data/data.json')
print twitter.pedido(params={"marca": "Ford", "modelo": "Mustang"})