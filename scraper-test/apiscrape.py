#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir,remove
import sys
import ijson
import operator
from pprint import pprint
import string

removed = "This message has been removed by ."

wordcount = {}

data = {"threads" : 0,
        "comments" : 0,
        "wordpairs" : 0}
def search_keywords(string, keywords):
    for word in keywords:
        if word in string.lower():
            return True
        return False
def addword(word):
    if word not in wordcount:
        wordcount[word] = 0
    wordcount[word] += 1

def writeToFile():
    try:
        remove("logs.txt")
    except OSError:
        pass
    sorted_wc = sorted(wordcount.items(),key=operator.itemgetter(1),reverse=True)
    with open("logs.txt","a") as f:
        f.write("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
        f.write("Most common wordpairs in text: \n\n")
        for i in range(0,150):
            f.write("%s,%s,%i\n" %(sorted_wc[i][0][0],sorted_wc[i][0][1],sorted_wc[i][1]))
        f.close()

toberemoved = ["<p>","</p>",",",".","?","!"]

keyword_file = open("./finnish_keywords.txt","r")
sents = keyword_file.read().split(",")
keywords = sents[0].split("\n")
keyword_file.close()

#f = json.load(open(sys.argv[1]))
righttopics = ["Paikkakunnat","Terveys"]
stopwords_file = open("./finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()
#pprint(stopwords)
files = listdir("./textdumps")
punc = set(string.punctuation)

i=0


def checkBody(string):
    returned=" "
    if "http" in string:
        #print("http found")
        return returned
    for w in toberemoved:
        if w in string:
            #print(string)
            returned = string.replace(w,"")
            return checkBody(returned)
    return string

def checkTopic(topics,righttopics):
    for topic in topics:
        #print(topic["title"])
        if topic["title"] in righttopics:
            #print(topic["title"])
            return False
    return True

def addSentence(w):
    cnt = len(w)
    for i in range(0,cnt):
        for j in range(i+1,cnt):
            if w[i]!=w[j] and w[i] not in punc and w[i] != " " and w[j] not in punc and w[j] != " ":
                if len(w[j])>3 and len(w[i])>3:
                    addword((w[i],w[j]))



for fileN in files:
    if fileN.endswith(".json"):
        filename="./textdumps/{}".format(fileN)
    else:
        continue

    #filename="./textdumps/dump10100-10199.json"
    with open(filename) as f:
        print(filename)
        try:
            items = ijson.items(f,"item")
            for o in items:
                #i+=1
                #print("analyzing object %i" %(i))
                body = o["body"]
                body = checkBody(body)
                #print(body)
                if checkTopic(o["topics"],righttopics):
                    #print("notRight")
                    continue
                if (search_keywords(body,keywords)==True) and body != removed:
                    data["threads"]+=1
                    clean = [word for word in body.split() if word.lower() not in stopwords]
                    addSentence(clean)
                else:
                    continue
                for c in o["comments"]:
                    sent = c["body"]
                    if (search_keywords(body,keywords)==True) and body != removed:
                        data["comments"]+=1
                        #print(body)
                        cleanC = [word for word in body.split() if word.lower() not in stopwords]
                        #print(cleanC)
                        addSentence(cleanC)

        except ValueError:
            print("ValueError")
            continue
        except ijson.common.IncompleteJSONError:
            print("IncompleteJSONError")
            continue
        writeToFile()

#pprint(data)
