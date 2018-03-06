import os 
import sys 
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

fread = open("sample.txt","r")
fwrite = open("output.txt","w+")

for line in fread.readlines():
    tweet_data = json.loads(line)
    if("extended_tweet") in tweet_data:
                tweet_count = tweet_count+ 1
                tweet= tweet_data['extended_tweet']['full_text']
                print(tweet_count)
                print(tweet)
                fwrite.write(data)
                status()         
            else:
                tweet_count = tweet_count+ 1
                tweet= tweet_data['text']
                print(tweet_count)
                print(tweet)
                fwrite.write(data)
                status()
