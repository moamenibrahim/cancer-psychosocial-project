import tweepy
import sys
import jsonpickle
import json
import os
from tweepy import OAuthHandler
from keywords_helper import cancer_keywords as cancer


maxTweets = 100000000  # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits

searchQuery = ' OR '.join(str(e) for e in cancer.lung)
print(searchQuery)

fName = 'lung_tweets.json'  # We'll store the tweets in a text file.

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit,
# start from the most recent tweet matching the search query.

max_id = -1
sinceId = None

consumer_key = 'zgwY6GgJ2p6kCX39X17zm4UpK'
consumer_secret = 'Kv9AazgJmYueIQPmY5kO1MhUsZvDiXaHJZw03fVe9p8H5AipPv'
access_token = '837798738907312132-p2OZgzDDF7ZeNBMKQ9l5f9XGdMlH1J8'
access_secret = 'wHQFCa7MedvYkF9jtWNtu6rpGMOCXQR7Ptq5jsFKrAbEv'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

downloaded_tweets = 0
tweetCount = 0

print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(
                        q=searchQuery, count=tweetsPerQry,
                        tweet_mode="extended", place="07d9cd6afd884001")
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId, tweet_mode="extended")
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1), tweet_mode="extended")
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId, tweet_mode="extended")
            if not new_tweets:
                print("No more tweets found")
                break

            # str_lst=["Finland","Sweden","Suomi"]
            for tweet in new_tweets:
                if tweet._json['user']['location'] != "":
                    # if  any(tweet._json['user']['location'] in s for s in str_lst) :
                    # if ('Finland' in (tweet._json['user']['location'])):
                    f.write(jsonpickle.encode(
                        tweet._json, unpicklable=False)+'\n')

                    downloaded_tweets = downloaded_tweets+1
                    print(tweet._json['full_text'])

                    tweetCount += len(new_tweets)
                    print("searched {0} tweets".format(tweetCount))
                    max_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print("downloaded {0} tweets, Saved to {1}".format(downloaded_tweets, fName))
