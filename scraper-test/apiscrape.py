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

#check if one of the keywords exist in the given string
def search_keywords(string, keywords):
    for word in keywords:
        if word in string.lower():
            return True
        return False
#helper function to add word into the dictionary
def addword(word):
    if word not in wordcount:
        wordcount[word] = 0
    wordcount[word] += 1
#writing out to log-file the current contents of wordcount
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

#Load keywords and stopwords, and define characters to be removed
toberemoved = ["<p>","</p>",",",".","?","!"]

keyword_file = open("./finnish_keywords.txt","r")
sents = keyword_file.read().split(",")
keywords = sents[0].split("\n")
keyword_file.close()


righttopics = ["Paikkakunnat","Terveys"]
stopwords_file = open("./finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()
#location of json folder to read data from
files = listdir("./textdumps")
punc = set(string.punctuation)

#simple checking if the string contains wrong messages
def checkBody(string):
    returned=" "
    if "http" in string:
        return returned
    for w in toberemoved:
        if w in string:
            returned = string.replace(w,"")
            return checkBody(returned)
    return string
#Check if the thread is in the correct topics
def checkTopic(topics,righttopics):
    for topic in topics:
        if topic["title"] in righttopics:
            return False
    return True
#Handling final checks of the sentences before actual words are added
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

    with open(filename) as f:
        print(filename)
        try:
            items = ijson.items(f,"item")
            for o in items:
                body = o["body"]
                body = checkBody(body)

                if checkTopic(o["topics"],righttopics):
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
                        cleanC = [word for word in body.split() if word.lower() not in stopwords]
                        addSentence(cleanC)

        except ValueError:
            print("ValueError")
            continue
        except ijson.common.IncompleteJSONError:
            print("IncompleteJSONError")
            continue
        writeToFile()

#pprint(data)
