import sys
import tweepy
import os 

consumer_key = 'zgwY6GgJ2p6kCX39X17zm4UpK'
consumer_secret = 'Kv9AazgJmYueIQPmY5kO1MhUsZvDiXaHJZw03fVe9p8H5AipPv'
access_token = '837798738907312132-p2OZgzDDF7ZeNBMKQ9l5f9XGdMlH1J8'
access_secret = 'wHQFCa7MedvYkF9jtWNtu6rpGMOCXQR7Ptq5jsFKrAbEv'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
fName="output.txt"
f= open(fName,"w+")

## source: https://www.cancer.gov/types
terms=["cancer","Tumor","Leukemia","Neuroblastoma","Paraganglioma","Retinoblastoma","Astrocytomas","Retinoblastoma","Lymphoma","Melanoma"]

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print (status.text)
        f.write(status.text)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())    
sapi.filter(track=["cancer" or "Tumor" or "Leukemia" or "Neuroblastoma" or "Paraganglioma" or "Retinoblastoma" or "Astrocytomas" or "Retinoblastoma" or "Lymphoma" or "Melanoma"],locations=[4.10,54.44,31.46,71.15])
