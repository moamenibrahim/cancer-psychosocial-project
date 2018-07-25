import tweepy
import sys
import jsonpickle
import json
import os
from tweepy import OAuthHandler

mylist = [  
            "cancer",
            "tumor",
            "leukemia",
            "neuroblastoma",
            "paraganglioma",
            "retinoblastoma",
            "astrocytomas",
            "retinoblastoma",
            "lymphoma",
            "melanoma",
            "syöpä",
            "kasvain",
            "säteily",
            "hoito",
            "kuolla",
            "malignant",  
            "metastasis", 
            "oncology",   
            "oncologist",
            "pathologist",
            "precancerous",
            "sarcoma",
            "telemedicine",
            "healthcare",
            "chemotherapy",
            "radiation",
            "hormonetherapy",
            "mammogram",
            "kræft",
            "kreft",
            "carcino",
            "lymphom",
            "biopsy",
            "biopsies",
            "melano",
            "sarcoma",
            "dysplasia",
            "mammogr",
            "maligna",
            "metasta",
            "PET",
            "ablate",
            "ablation",

        ### SPECIFIC CANCER KEYWORDS
        "osteosarcoma",
        "ewing",
        "fibrosarcoma",
        "histiocytoma",
        "chordoma",
        "gastrointestinal",
        "tract",
        "colorectal",
        "colon",
        "lymphoma",
        "carcinoid",
        "carcinoma",
        "adenocarcinoma",
        "carcinoma",
        "sarcoma",
        "SCLC",
        "NSCLC",
        "ductal",
        "medullary",
        "phyllodes",
        "angiosarcoma",
        "mucinous",
        "colloid",
        "nipple",
        "lobular",
        "LCIS",
        "squamous",
        "carcinomas",
        "carcinoids",
        "lymphoma",
        "melanoma",
        "basal",
        "dermatology",
        "melanoma",
        "moles",
        "cavity",
        "pharynx",
        "larynx",
        "neoplasm",
        "neuroma",
        "astrocytoma",
        "chordoma",
        "CNS",
        "fibrocystic",
        "craniopharyngioma",
        "medulloblastoma",
        "meningioma",
        "metastatic",
        "oligodendroglioma",
        "pituitary",
        "neuroectodermal",
        "PNET",
        "schwannoma",
        "osteosarcoma",
        "ewing",
        "fibrosarcoma",
        "histiocytoma",
        "chordoma",
        "neuroblastoma",
        "wilms",
        "osteosarcoma",
        "retinoblastoma",
        "pediatric",
        "XRCC1",
        "EGFR",
        "KRas",
        "P53",
        "BRCA1",
        "benign"
            ]


## From: https://www.cancer.gov/types
stomach=[
    "stomach",
    "vatsa",
    "gastric",
    "digestive",
    "gastrointestinal",
    "tract",
    "colorectal",
    "colon",
    "adenocarcinoma",
    "lymphoma",
    "carcinoid"
]

breast=[
    "breast",
    "breastcancer",
    "tits",
    "boobs"
    "rinta",
    "carcinoma",
    "adenocarcinoma",
    "carcinoma",
    "situ",
    "sarcoma",
    "BRCA1",
    "ductal",
    "medullary",
    "phyllodes",
    "angiosarcoma",
    "mucinous",
    "colloid",
    "lobular",
    "LCIS",
    "nipple",
    "nipples"
]

lung=[
    "lung",
    "keuhko",
    "SCLC",
    "NSCLC",
    "squamous",
    "carcinomas",
    "bronchial"
]

skin=[
    "skin",
    "iho",
    "lymphoma",
    "melanoma",
    "basal",
    "dermatology",
    "melanoma",
    "moles"
]

blood=[
    "leukemia",
    "veri",
    "leucocythaemia",
    "leucocythaemias",
    "leucocythemia",
    "leucocythemia",
    "hematologic",
    "blood"
]

head_neck=[
    "pään",
    "kaulan",
    "head",
    "neck",
    "pharynx",
    "larynx"
]

brain=[
    "brain",
    "aviot",
    "astrocytoma",
    "chordoma",
    "CNS",
    "craniopharyngioma",
    "medulloblastoma",
    "meningioma",
    "metastatic",
    "oligodendroglioma",
    "pituitary",
    "Neuroectodermal",
    "PNET",
    "schwannoma"
]

bone=[
    "bone",
    "luu",
    "osteosarcoma",
    "ewing",
    "fibrosarcoma",
    "histiocytoma",
    "chordoma"
]

pediatric=[
    "pediatric",
    "childhood",
    "child",
    "kid",
    "neuroblastoma",
    "wilms",
    "osteosarcoma",
    "retinoblastoma"]


maxTweets = 100000000  # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits

searchQuery = ' OR '.join(str(e) for e in lung)
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
