#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir,remove
import sys
import ijson,json,operator
from pprint import pprint
import string
import nltk
import codecs
# reload(sys)
# sys.setdefaultencoding('utf8')
import re
from nltk.probability import FreqDist
sys.path.append('/scraper-test')
import finnish_keywords
# -*- coding: utf-8 -*-
import numpy as np 
import os
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import itertools

wordcount = {}
keywords = finnish_keywords.illness_list + finnish_keywords.financial_list + finnish_keywords.death_list + finnish_keywords.social_list + finnish_keywords.treatment_list

#check if one of the keywords exist in the given string
def search_keywords(string, keywords):
    for word in keywords:
        if word in string:
            return True
    return False

#Load keywords and stopwords, and define characters to be removed
toberemoved = ["<p>","</p>",",","?","!","-"]

keywords = finnish_keywords.illness_list + finnish_keywords.financial_list + finnish_keywords.death_list + finnish_keywords.social_list + finnish_keywords.treatment_list

righttopics = ["Paikkakunnat","Terveys"]
stopwords_file = open("scraper-test/finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()
#location of json folder to read data from
files = listdir("scraper-test/textdumps")
punc = set(string.punctuation)

#Check if the thread is in the correct topics
def checkTopic(topics,righttopics):
    for topic in topics:
        if topic["title"] in righttopics:
            return False
    return True

#Helper function to remove odd characters from single words
def checkWord(wrd):
    return re.sub(r'[^a-zA-Z0-9åäöÅÄÖ]','',wrd)

def checkSentence(string):
    ret = []
    sents = nltk.sent_tokenize(string)
    for s in sents:
        tmp = ""
        if "http" in s:
            continue

        tokens = nltk.word_tokenize(s)
        for w in tokens:
            w=checkWord(w)
            if len(w)<2:
                continue
            tmp+=w+" "

        ret.append(tmp)
    return ret

fdist=FreqDist()

for fileN in files:
    if fileN.endswith(".json"):
        filename="./scraper-test/textdumps/{}".format(fileN)
    else:
        continue
    with open(filename) as f:
        print(filename)
        try:
            items = ijson.items(f,"item")
            for o in items:
                if checkTopic(o["topics"],righttopics) or o["deleted"] is True:
                    continue
                body = o["body"]
                if search_keywords(body,keywords):
                    body = checkSentence(body)
                    for sentence in body:
                        ## NLTK freqdist
                        words = nltk.tokenize.word_tokenize(sentence)
                        fdist+=FreqDist(words)
            # print(fdist)
        except ValueError:
            print("ValueError")
            continue
        except ijson.common.IncompleteJSONError:
            print("IncompleteJSONError")
            continue

writefile=open("scraper-test/results.json", "w+")
myset=set(fdist.items())
sorted_x=sorted(myset, key=operator.itemgetter(1), reverse=True)
json.dump(sorted_x, writefile, ensure_ascii=True)
writefile.close()

stopwords_file = open("./finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()

myset=dict(myset)
myset=dict((k.lower(), v) for k,v in myset.items())
for elm in stopwords:
    if elm.lower() in myset:
        myset.pop(elm.lower())

most_common=sorted_x[0:12]
print("main list done")

cancer=[]
for string in myset.items():
    if u"%s"%str(string[0]) in keywords:
        cancer.append(string)
sorted_cancer=sorted(cancer, key=operator.itemgetter(1), reverse=True)
most_common_cancer=sorted_cancer[0:12]
print("cancer list done")

### LET'S PLOT
x=[]
y=[]
for key,value in most_common:
    x.append(key)
    y.append(value)
trace0 = go.Bar(
    x=x,
    y=y,
    name='most repeated words'
)
x=[]
y=[]
for key,value in most_common_cancer:
    x.append(key)
    y.append(value)
trace1 = go.Bar(
    x=x,
    y=y,
    name='most cancer words'
)
data = [trace0, trace1]
layout = go.Layout(
        barmode='group',
        title='Co-occurence of words',
        xaxis=dict(
            title='words',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Percentage of occurrence',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
)
fig = go.Figure(data=data,layout=layout)
py.plot(data, filename='suomi24-with-any-cancer')