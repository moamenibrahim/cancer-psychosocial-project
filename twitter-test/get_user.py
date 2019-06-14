from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import json

consumer_key = 'zgwY6GgJ2p6kCX39X17zm4UpK'
consumer_secret = 'Kv9AazgJmYueIQPmY5kO1MhUsZvDiXaHJZw03fVe9p8H5AipPv'
access_token = '837798738907312132-p2OZgzDDF7ZeNBMKQ9l5f9XGdMlH1J8'
access_token_secret = 'wHQFCa7MedvYkF9jtWNtu6rpGMOCXQR7Ptq5jsFKrAbEv'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


def printRoutine(inputTxt):
    """ Method to print in a file and on screen for debugging purposes """
    json.dump(inputTxt, f)
    f.write(' \n')


account_list = [53292926,  # Julie McCrossin
                99625563,  # Ann Silberman
                12511062,  # Barbara Jacoby
                144851483,  # Nancy's Point
                16157175,  # Nicole McLean
                374864146,  # Rann Patterson
                65594160]  # Dr. Gia Sison

# threshold 7 tweets , max 30
# account_list = [499649171, 499648091, 961153933, 3172336367, 2841368445, 738032030714318849, 497992988]
# account_list = [19939596, 832662336917811201, 872881071771324416, 53292926]


if len(account_list) > 0:
    for index, target in enumerate(account_list):
        print("Getting data for " + str(target))
        item = auth_api.get_user(target)
        print("name: " + item.name)
        print("screen_name: " + item.screen_name)
        print("description: " + item.description)
        print("statuses_count: " + str(item.statuses_count))
        print("friends_count: " + str(item.friends_count))
        print("followers_count: " + str(item.followers_count))

        tweets = item.statuses_count
        account_created_date = item.created_at
        delta = datetime.utcnow() - account_created_date
        account_age_days = delta.days
        print("Account age (in days): " + str(account_age_days))
        if account_age_days > 0:
            print("Average tweets per day: " + "%.2f" %
                  (float(tweets)/float(account_age_days)))

        f = open("twitter-test/get_user_"+str(index+1)+".json", "w+")

        hashtags = []
        mentions = []
        tweet_count = 0
        for status in Cursor(auth_api.user_timeline, id=target, count=99999999).items():
            tweet_count += 1
            if hasattr(status, "entities"):
                entities = status.entities
                if "hashtags" in entities:
                    for ent in entities["hashtags"]:
                        if ent is not None:
                            if "text" in ent:
                                hashtag = ent["text"]
                            if hashtag is not None:
                                hashtags.append(hashtag)
                if "user_mentions" in entities:
                    for ent in entities["user_mentions"]:
                        if ent is not None:
                            if "screen_name" in ent:
                                name = ent["screen_name"]
                            if name is not None:
                                mentions.append(name)
                printRoutine({"created at": status.created_at.__str__(
                ), "text": status._json['text'], "entities": status.entities})

        print("Most mentioned Twitter users:")
        for item, count in Counter(mentions).most_common(10):
            print(item + "\t" + str(count))

        print("Most used hashtags:")
        for item, count in Counter(hashtags).most_common(10):
            print(item + "\t" + str(count))

        print("All done. Processed " + str(tweet_count) + " tweets.")
        print("--------------------------")

f.close()
