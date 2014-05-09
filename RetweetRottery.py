#!/usr/bin/python

import sys
import tweepy
import time
from tweepy.auth import OAuthHandler
from tweepy.api import API


class myExeption(Exception):
    pass


def get_debug_auth():
    consumer_key = "o7vgHO8hRGPl62L9xokp76Fan"
    consumer_secret = "DuBOE39WluGJeRdUtz3sXAN7pjPr4mtoaRJYe5IueIRaeOejID"
    access_key = "2202914137-2Wp8TUV0a2fRStUuyVsVVgRFHgOyUJsGgZcaGia"
    access_secret = "UmElmxLECaF6pTx4Q11KVAs2s9Tvlp0aeBJLLYaBfzXzR"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth


class Auth:
    apikey = "o7vgHO8hRGPl62L9xokp76Fan"
    apisecret = "DuBOE39WluGJeRdUtz3sXAN7pjPr4mtoaRJYe5IueIRaeOejID"
    oauth = None
    api = None
    tweetid = None

    def __init__(self):
        oauth = tweepy.OAuthHandler(self.apikey, self.apisecret)
        try:
            redirect_url = oauth.get_authorization_url()
            print redirect_url
        except tweepy.TweepError:
            print 'Error! Failed to get request token.'
            return False

        verifier = raw_input('Verifier: ')
        try:
            oauth.get_access_token(verifier)
            return self.oauth
        except tweepy.TweepError:
            print 'Error! Failed to Get Access token'
            return False


class StreamListener(tweepy.streaming.StreamListener):
    tweet_id = None
    user_list = []

    def __init__(self, send_tweet_id):
        super(StreamListener, self).__init__()
        self.tweet_id = send_tweet_id 
    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            retweeted_id =  status.retweeted_status.id
            retweeted_count = status.retweeted_status.retweet_count
            retweeted_user = status.author
            user_name = retweeted_user.screen_name
            if self.tweet_id == retweeted_id:
                print user_name
                self.user_list.append(user_name) 

    def on_error(self, status):
        print "can't get"

    def on_timeout(self):
        raise myExeption


class Rottery:
    getauth = None
    tweetid = None
    timer = None

    def __init__(self, oauth):
        self.getauth = oauth
        self.getapi = tweepy.API(self.getauth)

    def Send(self, sendtweet, time):
        print time
        tweetobject = self.getapi.update_status(sendtweet)
        self.tweetid = tweetobject.id
        self.timer = time
        self.StreamingSerch()

    def StreamingSerch(self):
        listener = StreamListener(self.tweetid)
        stream = tweepy.Stream(self.getauth, listener, secure=True)
        stream.userstream(async=True)
        time.sleep(self.timer)
        stream.disconnect()

if __name__ == '__main__':
    authkey = get_debug_auth()
    user = Rottery(authkey)
    text = raw_input("Input Your Tweet : ")
    print "Wating 10 Sec..."
    time.sleep(10)
    user.Send(sendtweet=text, time=10)
