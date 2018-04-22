import os
import sys
import json
import re
import string
import subprocess
import nltk
import operator
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from lda_topic import lda_modeling
from googletrans import Translator
from nltk.tokenize import RegexpTokenizer
from os.path import expanduser
from nltk.tag import StanfordPOSTagger  
from nltk.tag import StanfordNERTagger
from nltk.corpus import wordnet as wn

""" A list contains the query words to search for """
mylist = [  "cancer",
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
            "Malignant",  
            # Refers to a tumor that is cancerous
            "metastasis", 
            # Cancer spreading
            "oncology",   
            # Study of cancer 
            "oncologist",
            "pathologist",
            # Refers to cells that have the potential to become cancerous
            "precancerous",
            # A type of cancer
            "Sarcoma",
            "telemedicine",
            "healthcare",
            "chemotherapy",
            "mammogram",
            "Kræft",
            "kreft"]

""" list for family related keywords and queries """
family_list = [ "family",
                "sad",
                "love",
                "hate",
                "father",
                "son",
                "daughter",
                "mother",
                "boyfriend",
                "girlfriend",
                "spouse",
                "husband",
                "wife"]

""" list for friend related keywords and queries """
friend_list = ["friends",
               "friendship",
               "relation"]

""" list for money related keywords and queries """
money_list = ["money",
              "price",
              "dollars",
              "euros"]


def printRoutine(inputTxt):
    """ Method to print in a file and on screen for debugging purposes """

    # print(str(inputTxt))
    # f.write(str(inputTxt)+'\n')


def get_hashtags(tweet,tweet_count):
    # TODO 
    pass

def get_link(tweet,tweet_count):
    """ Extracting links from tweets or text """
    # TODO : determine the link info and know whether it can be helpful for
    # the study or no.

    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, tweet)
    if match:
        return match.group()
    return ''

def strip_links(text,data):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    data.append({'links':links})
    for link in links:
        text = text.replace(link[0], ' ')
    return text

def strip_all_entities(text):
    entity_prefixes = ['@', '#']
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def get_translate(input_str, lang):
    """ using googletrans to translate text from any language to English """

    if(lang != 'und'):
        try:
            translated = translator.translate(input_str, dest='en', src=lang)
            return translated.text
        except:
            printRoutine("Failed to translate text")
            return False

def get_pos(tweet):
    """ 
    part of speech tagging extraction
    """
    staged_rows={}
    text = word_tokenize(str(tweet))
    result_postag = nltk.pos_tag(text)
    # printRoutine(result_postag)
    for row in result_postag:
        if (row[1] != ''):
            if (row[1] in staged_rows):
                ## increment
                staged_rows[row[1]] += 1
            else:
                ## add to list
                staged_rows[row[1]] = 1

    printRoutine(sorted(staged_rows.items(),
                        key=operator.itemgetter(1), reverse=True))
    return result_postag

def get_stanford_pos(tweet):
    """
    part of speech tagging extraction
    TODO: standford tagger
    """
    home = expanduser("~")
    path_to_model = home + \
        '/work/cancer/stanford/stanford-postagger/models/english-bidirectional-distsim.tagger'
    path_to_jar = home + \
        '/work/cancer/stanford/stanford-postagger/stanford-postagger.jar'
    st = StanfordPOSTagger(path_to_model,path_to_jar=path_to_jar)
    result = st.tag(tweet.split())
    return result

# def get_Geniapos(tweet):
#     """ Genia Tagger part of speech tagging extraction
#     Medical part of speech tagger """
#     return tagger.parse(tweet)

def get_hyponyms(tweet):
    """ 
    hyponyms extraction and checking the topics list 
    TODO: wordnet vs wordvector
    """
    entities={}
    words=tweet.split()
    for word in words:
        for i, j in enumerate(wn.synsets(word)):
            entities["Meaning:"+str(i)+" NLTK ID:"+str(j.name())]
            entities["Meaning:"+str(i)+" NLTK ID:"+str(j.name())].append("Hyponyms: "+str(j.hyponyms()))
    return entities

def get_named_entity(tweet):
    """ 
    get named entity recognition and check if words have entry in lexical database 
    TODO: Illinois named entity
    """
    pass

def get_stanford_named_entity(tweet):
    """ 
    get named entity recognition and check if words have entry in lexical database 
    TODO: Stanford named entity
    """
    home = expanduser("~")
    stanford_dir = home + '/work/cancer/stanford/stanford-nertagger/'
    jarfile = stanford_dir + 'stanford-ner.jar'
    modelfile = stanford_dir + 'classifiers/english.all.3class.distsim.crf.ser.gz'
    st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)
    result = st.tag(tweet.split())
    return result

def visualize_results(input):
    """
    visualize obtained results 
    TODO: python tools
    """
    pass

# def get_topic(input_str):
#     """ Topic extraction from text using LDA (Latent Dirichet Allocation): 
#     It classifies the text according to whether it is family, friend, money related"""
#     try:
#         topic = lda.generate_topic(input_str)
#         if any(word in topic for word in family_list):
#             printRoutine("family related tweet: extracting emotions")
#             get_sentiment(input_str)
#         if any(word in topic for word in friend_list):
#             printRoutine("friend related tweet: extracting emotions")
#             get_sentiment(input_str)
#         if any(word in topic for word in money_list):
#             printRoutine("money related tweet")
#             get_sentiment(input_str)
#         return True
#     except:
#         printRoutine("Error getting topic")
#         return False

def analyze_location(fileName):
    """ Method to analyze file by file and calls all other methods """
    staged_location={}
    for line in fileName.readlines():

        tweet_data = json.loads(line)
        location = tweet_data['user']['location']
        if (location != ''):
            if (location in staged_location):
                ## increment that location
                staged_location[location] += 1
            else:
                ## add location to list
                staged_location[location] = 1
    return

def analyze_user(fileName):
    """ Method to analyze file by file and calls all other methods """
    staged_users={}
    for line in fileName.readlines():

        tweet_data = json.loads(line)
        user = tweet_data['user']['id']
        if (user != ''):
            if (user in staged_users):
                ## increment that user
                staged_users[user] += 1
            else:
                ## add user to list
                staged_users[user] = 1
    return

def analyze_file(fileName, tweet_count):
    """ Method to analyze file by file and calls all other methods """

    for line in fileName.readlines():
        tweet_data = json.loads(line)
        if("extended_tweet") in tweet_data:
            tweet = tweet_data['extended_tweet']['full_text']
        else:
            tweet = tweet_data['text']

        if any(word in tweet for word in mylist):
            tweet_count = tweet_count + 1
            # printRoutine('------------------------------------------------------')
            printRoutine(str(tweet_count))
            # printRoutine(tweet)
            data['tweet'+str(tweet_count)]
            # printRoutine(tweet_data['lang'])
            data['tweet'+str(tweet_count)].append({'lang':tweet_data['lang']})
            pure_text = strip_all_entities(strip_links(tweet))
            translated = get_translate(pure_text, tweet_data['lang'])

            if translated:
                printRoutine(translated)
                data['tweet'+str(tweet_count)].append({'translation':translated})
                pos=get_pos(translated)
                data['tweet'+str(tweet_count)].append({'pos':pos})
                printRoutine(get_stanford_pos(translated))
                hyponyms=get_hyponyms(translated)
                data['tweet'+str(tweet_count)].append({'hyponyms':hyponyms})
                named = get_stanford_named_entity(translated)
                data['tweet'+str(tweet_count)].append({'named entity':named})

    return int(tweet_count)


if __name__ == "__main__":

    translator = Translator()
    f = open("stream_results.json", "w+")

    data={}

    tweet_count = 0

    for x in range(3,7):
        fread = open("outputDir/2018-03-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)
    f.close()
