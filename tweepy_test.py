import tweepy
from tweepy import OAuthHandler
from googletrans import Translator 

translator=Translator()
 
consumer_key = 'zgwY6GgJ2p6kCX39X17zm4UpK'
consumer_secret = 'Kv9AazgJmYueIQPmY5kO1MhUsZvDiXaHJZw03fVe9p8H5AipPv'
access_token = '837798738907312132-p2OZgzDDF7ZeNBMKQ9l5f9XGdMlH1J8'
access_secret = 'wHQFCa7MedvYkF9jtWNtu6rpGMOCXQR7Ptq5jsFKrAbEv'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

user = api.get_user('twitter')

results= api.search(q="syöpä",count= 50) 
for result in results:
    print("Tweet:")
    print(result.text)
    print(translator.translate(result.text))