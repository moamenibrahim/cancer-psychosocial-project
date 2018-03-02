import sys
import tweepy
import os 
import json
from subprocess import call 

consumer_key = 'zgwY6GgJ2p6kCX39X17zm4UpK'
consumer_secret = 'Kv9AazgJmYueIQPmY5kO1MhUsZvDiXaHJZw03fVe9p8H5AipPv'
access_token = '837798738907312132-p2OZgzDDF7ZeNBMKQ9l5f9XGdMlH1J8'
access_secret = 'wHQFCa7MedvYkF9jtWNtu6rpGMOCXQR7Ptq5jsFKrAbEv'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
fName ="output.txt"
f = open(fName,"w+")

## source: https://www.cancer.gov/types
## use track and include OR in between 
terms=["cancer","Tumor","Leukemia","Neuroblastoma","Paraganglioma","Retinoblastoma","Astrocytomas","Retinoblastoma","Lymphoma","Melanoma"]


class CustomStreamListener(tweepy.StreamListener):

    '''
    create the stream listener and get status, error and timeout issues
    '''

    def __init__(self):
        self.tweet_count = 0
        pass

    def on_status(self, status):
        return
        
    def on_data(self,data):
        tweet_data = json.loads(data)
        if("extended_tweet") in tweet_data:
            self.tweet_count = self.tweet_count+ 1
            tweet= tweet_data['extended_tweet']['full_text']
            print(self.tweet_count)
            print(tweet)
            f.write(tweet)
        return

    def on_error(self, status_code):
        if status_code == 420: #Returning False in on_data disconnects the stream
            return False
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


sapi = tweepy.streaming.Stream(auth, CustomStreamListener(), tweet_mode= 'extended')    
sapi.filter(locations=[2.43,55.30,36.58,70.39], async=True)


