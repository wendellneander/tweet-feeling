import tweepy
import time
import re
from textblob import TextBlob
from credentials import *


class Twitter():

    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        self.auth = tweepy.OAuthHandler(api_key, api_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

    def get_timeline(self):
        public_tweets = self.api.home_timeline()
        return public_tweets

    def get_tweets_from_user(self, username):
        public_tweets = self.api.user_timeline(id=username)
        return public_tweets

    def get_user(username):
        return api.get_user(username)
        #print(user.screen_name)
        #print(user.followers_count)

    def get_followers():
        followers = []
        for follower in self._limit_handled(tweepy.Cursor(self.api.followers).items()):
            followers.append(follower)
            #print(follower.screen_name)
                
        return followers
        
    def _limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                time.sleep(15 * 60)


class TweetAnalyzer():

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        tweet = self.clean_tweet(tweet)
        if len(tweet) < 3:
            return 0

        blob = TextBlob(tweet)
        from_language = blob.detect_language()

        if from_language != 'en':
            try:
                blob.translate(from_lang=from_language, to='en')
            except BaseException as e:
                pass
        
        print(blob.sentiment.polarity, str(blob), tweet)

        if blob.sentiment.polarity > 0:
            return 1
        elif blob.sentiment.polarity == 0:
            return 0
        else:
            return -1


if __name__ == '__main__':

    twitter_client = Twitter(api_key, api_secret, access_token, access_token_secret)
    twitter_analyzer = TweetAnalyzer()
    
    for tweet in twitter_client.get_timeline():
        twitter_analyzer.analyze_sentiment(tweet.text)