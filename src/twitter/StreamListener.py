import sys
import tweepy
import os
import json
from subprocess import call
from datetime import datetime


consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

outputDir = "outputDir"


class CustomStreamListener(tweepy.StreamListener):

    '''
    create the stream listener and get status, error and timeout issues
    '''

    def __init__(self):
        super(CustomStreamListener, self).__init__(self)
        self.basePath = outputDir
        os.system("mkdir -p %s" % (outputDir))

        d = datetime.today()
        self.filename = "%i-%02d-%02d.json" % (d.year, d.month, d.day)
        # open for appending just in case
        self.fh = open(self.basePath + "/" + self.filename, "a")

        self.errorCount = 0
        self.limitCount = 0
        self.last = datetime.now()
        self.tweet_count = 0
        return

    def on_data(self, data):
        tweet_data = json.loads(data)
        if("extended_tweet") in tweet_data:
            self.tweet_count = self.tweet_count + 1
            tweet = tweet_data['extended_tweet']['full_text']
            print(self.tweet_count)
            print(tweet)
            self.fh.write(data)
            self.status()
        else:
            self.tweet_count = self.tweet_count + 1
            tweet = tweet_data['text']
            print(self.tweet_count)
            print(tweet)
            self.fh.write(data)
            self.status()
        return True

    def status(self):
        now = datetime.now()
        if (now-self.last).total_seconds() > 300:
            print("%s - %i tweets, %i limits, %i errors in previous five minutes." %
                  (now, self.tweet_count, self.limitCount, self.errorCount))
            self.tweetCount = 0
            self.limitCount = 0
            self.errorCount = 0
            self.last = now
            self.rotateFiles()  # Check if file rotation is needed

    def on_error(self, status_code):
        if status_code == 420:  # Returning False in on_data disconnects the stream
            return False
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

    def rotateFiles(self):
        print("rotating file")
        d = datetime.today()
        filenow = "%i-%02d-%02d.json" % (d.year, d.month, d.day)
        if (self.filename != filenow):
            print("%s - Rotating log file. Old: %s New: %s" %
                  (datetime.now(), self.filename, filenow))
            try:
                self.fh.close()
            except:
                pass
            self.filename = filenow
            self.fh = open(self.basePath + "/" + self.filename, "a")

    def close(self):
        try:
            self.fh.close()
            print("files closed")

        except:
            pass


if __name__ == "__main__":
    try:
        sapi = tweepy.streaming.Stream(
            auth, CustomStreamListener(), tweet_mode='extended')
        sapi.filter(locations=[2.43, 55.30, 36.58, 70.39], async=True)
    except KeyboardInterrupt:
        sapi.close()
