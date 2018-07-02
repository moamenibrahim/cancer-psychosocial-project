#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir,remove
import sys
import ijson
#import operator
from pprint import pprint
import string
import nltk
import finnish_keywords as keywords
import re
import pyrebase
import datetime


pyrebase_config = {
    "apiKey": "AIzaSyBIJYd5Xxa7DIORsLPJUCT2r4DqUa_bxlo",
    "authDomain": "analysis-820dc.firebaseapp.com",
    "databaseURL": "https://analysis-820dc.firebaseio.com",
    #projectId: "analysis-820dc",
    "storageBucket": "analysis-820dc.appspot.com",
    #messagingSenderId: "863565878024",
    "servicAccount": "./firebase-config/config.json"
}

firebase = pyrebase.initialize_app(pyrebase_config)
db = firebase.database()

wordcount = {}

#kw=db.child("keywords").get()

data = {"threads" : 0,
        "comments" : 0,
        "wordpairs" : 0}

def pushFirebase(table,json_data):
    db.child(table).push(json_data)

def updateFirebase(table,entry,json_data):
    db.child(table).child(entry).update(json_data)

def delFirebase(table,entry):
    db.child(table).child(entry).remove()



#check if one of the keywords exist in the given string
def search_keywords(string):
    keywords_found=[]
    #keywords_found={"death":0,"illness":0,"treatment":0,"social":0,"financial":0}
    for word in kw.val()["death"]:
        if word in string.lower():
            keywords_found.append("death")
            #keywords_found["death"]=1
            break
    for word in kw.val()["illness"]:
        if word in string.lower():
            keywords_found.append("illness")
            #keywords_found["illness"]=1
            break
    for word in kw.val()["treatment"]:
        if word in string.lower():
            keywords_found.append("treatment")
            #keywords_found["treatment"]=1
            break
    for word in kw.val()["social"]:
        if word in string.lower():
            keywords_found.append("social")
            #keywords_found["social"]=1
            break
    for word in kw.val()["financial"]:
        if word in string.lower():
            keywords_found.append("financial")
            #keywords_found["financial"]=1
            break
    return keywords_found

#helper function to add word into the dictionary
def addword(word,dist,topics,comment,time,nicknames):
    if dist>25:
        return
    if word not in wordcount:
        wordcount[word] = {}
        wordcount[word]["wordDistance"]=addDistance(dist)
        wordcount[word]["subforums"]=formatIntoDict(topics)
        #wordcount[word]["keyWords"]=formatIntoDict(foundKeywords)
        wordcount[word]["isComment"]=isComment(comment)
        wordcount[word]["nicknames"]=formatIntoDict(nicknames)
        wordcount[word]["postTimes"]=formatIntoDict(time)
    else:
        vals = addDistance(dist)
        #kvals = formatIntoDict(foundKeywords)
        tvals = formatIntoDict(topics)
        nvals = formatIntoDict(nicknames)
        timevals=formatIntoDict(time)
        cvals = isComment(comment)
        obj = wordcount[word]
        addStuff(obj["wordDistance"],vals)
        #addStuff(obj["keyWords"],kvals)
        addStuff(obj["subforums"],tvals)
        addStuff(obj["nicknames"],nvals)
        addStuff(obj["postTimes"],timevals)
        addStuff(obj["isComment"],cvals)

def isComment(b):
    if b:
        return {"inComments":1}
    else:
        return {"inTopic":1}

def addStuff(obj,vals):
    for k in vals:
        try:
            obj[k] += vals[k]
        except KeyError:
            obj[k] = vals[k]

def formatIntoDict(items):
    itemList={}
    for w in items:
        itemList[w]=1
    return itemList

def addDistance(dist):
    #a = {"1-2":0,"3-5":0,"6-8":0,"8-14":0,"15+":0}
    a={}
    if dist<3:
        a["1-2"]=1
    elif dist<6:
        a["3-5"]=1
    elif dist<9:
        a["6-8"]=1
    elif dist<15:
        a["8-14"]=1
    else:
        a["15+"]=1
    return a

def addNewValues(dbobj,newobj):
    addStuff(dbobj["wordDistance"],newobj["wordDistance"])
    addStuff(dbobj["topics"],newobj["topics"])
    #addStuff(dbobj["keyWords"],newobj["keyWords"])
    return dbobj

def writeToDatabase():
    for key,val in sorted(wordcount.items(), key=lambda i:sum(i[1]["wordDistance"].values()),reverse=True):
        try:
            currVals=db.child("co-occurrences-all").child("%s-%s"%(key[0],key[1])).get()
            retVal=addNewValues(currVals.val(),val)
            db.child("co-occurrences-all").child("%s-%s"%(key[0],key[1])).update(retVal)
        except:
            try:
                db.child("co-occurrences-all").child("%s-%s"%(key[0],key[1])).set(val)
            except:
                continue
#writing out to log-file the current contents of wordcount
def writeToFile():
    try:
        remove("logs.txt")
    except OSError:
        pass
    #print(wordcount)
    #sorted_wc = sorted(wordcount.items(),key=operator.itemgetter(1),reverse=True)
    #pprint(wordcount)

    with open("logs.txt","a") as f:
        f.write("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
        f.write("Most common wordpairs in text: \n\n")
        #r= 250 if len(sorted_wc) > 250 else len(sorted_wc)
        #for i in range(0, r):,keyword
        i = 0
        for key,val in sorted(wordcount.items(), key=lambda i:sum([i[1]['1-2'],i[1]['3-5'],i[1]['6-8'],i[1]['8-14'],i[1]['15+']]),reverse=True):
            #print(key,val)
            f.write("%s,%s,\n\t\t'total': %i,\n\t\t'1-2': %i, \n\t\t'3-5': %i, \n\t\t'6-8': %i,\n\t\t'8-14': %i,\n\t\t'15+': %i\n\t\t" %
            (key[0],key[1],sum([val['1-2'],val['3-5'],val['6-8'],val['8-14'],val['15+']]),
            val['1-2'],val['3-5'],val['6-8'],val['8-14'],val['15+']))
            f.write("keywords: \n")
            for k in val["keyWords"]:
                f.write("\t\t\t%s: %i\n"%(k,val["keyWords"][k]))
            f.write("Topics: \n")
            for v in val:
                if v not in ['1-2','3-5','6-8','8-14','15+','keyWords']:
                     f.write("\t\t\t%s : %i\n"% (v,val[v]))
            f.write("\n")
            if (i>300):
                break
            i+=1
        f.close()

#def

#Load keywords and stopwords, and define characters to be removed
toberemoved = ["<p>","</p>",",","?","!","-"]
"""
keyword_file = open("./finnish_keywords.txt","r")
sents = keyword_file.read().split(",")
keywords = sents[0].split("\n")
keyword_file.close()
"""

righttopics = ["Terveys"]
#rightSubtopics=["Syöpä",""]
stopwords_file = open("./finnish_stopwords.txt","r")
lines = stopwords_file.read().split(",")
stopwords = lines[0].split("\n")
stopwords_file.close()
#location of json folder to read data from
files = listdir("./textdumps")
punc = set(string.punctuation)

#simple checking if the string contains wrong messages

#Check if the thread is in the correct topics
def checkTopic(topics,righttopics):
    for topic in topics:
        if topic["title"] in righttopics:
            return False
            #return checkSubtopic(topics)
    return True

#def checkSubtopic(topics)

#helper function to extract onlif keywords_found:

def extractTopics(topics):
    retTopics=[]
    for t in topics:
        retTopics.append(t["title"])
    return retTopics

#Handling final checks of the sentences before actual words are added
def addSentence(w,topics,comment,time,nicknames):
    #print(w)
    wordlist=[word for word in w.split()]
    for i in range(len(wordlist)):
        for j in range(i+1,len(wordlist)):
            #print("test1")
            #print(wordlist[i],wordlist[j])
            if wordlist[i] == "<poistettu>" or wordlist[j] == "<poistettu>":
                continue
            if len(wordlist[i]) > 2 and len(wordlist[j]) > 2 and wordlist[i]!=wordlist[j] and wordlist[i] != " " and wordlist[j] != " ":
                #print("test2")
                addword((wordlist[i],wordlist[j]),j-i,topics,comment,time,nicknames)



#Helper function to remove odd characters from single words
def checkWord(wrd):
    return re.sub(r'[^\w0-9]','',wrd)

def checkSentence(string):
    ret = []
    sents = nltk.sent_tokenize(string)
    for s in sents:
        tmp = ""
        if "http" in s or "json" in s:
            #print("http")
            continue
        tokens = nltk.word_tokenize(s)
        for w in tokens:
            w=checkWord(w)
            w=w.lower()
            if w in stopwords:
                #print(w)
                tmp+="<poistettu>"+" "
                continue
            tmp+=w+" "
        ret.append(tmp)
    return ret

def getValueIntoList(val):
    ret = []

    ret.append(val)
    return ret
def getDateString(unixts):
    obj=[]
    d=datetime.datetime.fromtimestamp(unixts/1000).strftime("%m-%Y")
    obj.append(d)
    return obj


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
                if o["deleted"] is True:
                    #checkTopic(o["topics"],righttopics) or #extra check above
                    #print(o["topics"],o["deleted"])
                    continue
                topics=extractTopics(o["topics"])
                body = o["body"]
                #foundKeywords = search_keywords(body)
                #if foundKeywords:
                    #fKeyWords = foundKeywords.copy()
                body = checkSentence(body)
                timestamp = getDateString(o["created_at"])
                anonnick = getValueIntoList(o["anonnick"])

                for sentence in body:
                    wordcount={}
                    data["threads"]+=1
                    #clean = [word for word in sentence.split() if word.lower() not in stopwords]
                    #print(foundKeywords)
                    #print(timestamp,anonnick)
                    addSentence(sentence,topics,False,timestamp,anonnick)
                    writeToDatabase()
                for c in o["comments"]:
                    if c["deleted"] is True:
                        continue
                    sent = c["body"]
                    #if (search_keywords(s,keywords)==True):
                    sent = checkSentence(sent)
                    timestamp = getDateString(c["created_at"])
                    anonnick = getValueIntoList(c["anonnick"])
                    for s in sent:
                        wordcount={}
                        data["comments"]+=1
                        #cleanC = [word for word in body.split() if word.lower() not in stopwords]
                        #print(timestamp2,anonnick2)
                        addSentence(s,topics,True,timestamp,anonnick)
                        writeToDatabase()
        except ValueError:
            print("ValueError")
            continue
        except ijson.common.IncompleteJSONError:
            print("IncompleteJSONError")
            continue


    #writeToDatabase()
    #writeToFile()

#pprint(data)
print("Threads: %s,Comments: %s\n" %(data["threads"],data["comments"]))
