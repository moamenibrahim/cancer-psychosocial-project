import os 
import sys 
import json
import re
import geniatagger
import string
import time
import pyrebase
import urllib
import mimetypes
import subprocess
import nltk 
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from lda_topic import lda_modeling
from ibmNLPunderstanding import AlchemyNLPunderstanding
from googletrans import Translator
from nltk.tokenize import RegexpTokenizer

""" Configuration for the firbase database settings """ 
config = { 
    "apiKey": "AIzaSyBIJYd5Xxa7DIORsLPJUCT2r4DqUa_bxlo",
    "authDomain": "analysis-820dc.firebaseapp.com",
    "databaseURL": "https://analysis-820dc.firebaseio.com",
    "projectId": "analysis-820dc",
    "storageBucket": "analysis-820dc.appspot.com",
    "messagingSenderId": "863565878024",
    "serviceAccount": "/home/moamen/work/cancerDashboard/key.json"
} 

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
friend_list =["friends",
              "friendship",
              "relation"]
              
""" list for money related keywords and queries """
money_list =["money",
             "price",
             "dollars",
             "euros"]


def funcname(parameter_list):
    pass

def funcname(parameter_list):
    pass

def databasePush(tweet_count, tweet_data):
    """ A method to send tweets without processed data 
    to the database on firebase """

    db.child("Twitter").child("tweet"+str(tweet_count))
    db.set(tweet_data)
    pass

def remove_stopWords(tweet):
    """ Removing english stop words from the text sent 
    including punctuations """

    exclude = set(string.punctuation)
    word_tokens = word_tokenize(tweet)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    punc_free = ' '.join(ch for ch in filtered_sentence if ch not in exclude)
    return filtered_sentence


def finnishParse(tweet, tweet_count):
    """ Parsing Finnish words and text, the library was developed by 
    univerity of Turku, it performs sentence splitting, tokenization, tagging, parsing """
        
    wd = os.getcwd()
    os.chdir("/home/moamen/work/cancer_material/Finnish-dep-parser")
    with open('finnParse.txt', 'w+') as f:
            f.write(tweet)
    subprocess.call('cat finnParse.txt | ./parser_wrapper.sh > output.conllu', shell=True)
    subprocess.call('cat output.conllu | python split_clauses.py > output_clauses.conllu', shell=True)
    subprocess.call(
        'cat output_clauses.conllu | python visualize_clauses.py > output_clauses'+str(tweet_count)+'.html', shell=True)
    with open('output.conllu','r') as f:
        parse_result = f.readline()
    os.chdir(wd)
    return parse_result

def remove_finnstopWords(tweet):
    """ Removing Finnish stop words from the text sent 
    including links removal """

    stopwords_file = open("./finnish_stopwords.txt", "r")
    lines = stopwords_file.read().split(",")
    stopwords = lines[0].split("\n")
    tokenizer = RegexpTokenizer(r'\w+')
    texts = []
    raw = tweet.decode().lower()
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = [i for i in tokens if not i in stopwords and len(i) != 1]
    texts.append(stopped_tokens)
    return stopped_tokens

def get_topic(input_str):
    """ Topic extraction from text using LDA (Latent Dirichet Allocation): 
    It classifies the text according to whether it is family, friend, money related"""
    
    try:
        topic = lda.generate_topic(input_str)
        if any(word in topic for word in family_list):
            printRoutine("family related tweet: extracting emotions")
            get_sentiment(input_str)
        
        if any(word in topic for word in friend_list):
            printRoutine("friend related tweet: extracting emotions")
            get_sentiment(input_str)

        if any(word in topic for word in money_list):
            printRoutine("money related tweet")
            get_sentiment(input_str)
        return True
    except:
        printRoutine("Error getting topic")
        return False


def get_translate(input_str,lang):
    """ using googletrans to translate text from any language to English """

    if(lang!='und'):
        try:
            translated=translator.translate(input_str, dest='en', src=lang)
            return translated.text
        except:
            printRoutine("Failed to translate text")
            return False


def get_Geniapos(tweet):
    """ Genia Tagger part of speech tagging extraction
    Medical part of speech tagger """

    out = tagger.parse(tweet)
    printRoutine(out)


def get_pos(tweet):
    """ part of speech tagging extraction """

    text = word_tokenize(str(tweet))
    return nltk.pos_tag(text)


def get_sentiment(input_str):
    """ Get sentiment analysis when needed, the used API is IBM watson's """

    NLP_understanding.get_response(input_str)


def extract_link(text):
    """ Extracting links from tweets or text """
    # TODO : determine the link info and know whether it can be helpful for
    # the study or no. 

    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''


def guess_type_of(link, strict=True):
    """ Determine the link info and know whether it can be helpful for
    the study or no """

    link_type, _ = mimetypes.guess_type(link)
    print(link_type)

    with urllib.request.urlopen(link) as response:
        html = response.read()
        if link_type is None and strict:
            u = urllib.request.urlopen(link)
            link_type = html.info().gettype()  
            # or using: u.info().gettype()
    return html


def printRoutine(inputTxt):
    """ Method to print in a file and on screen for debugging purposes """

    print(str(inputTxt))
    f.write(str(inputTxt)+'\n')


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
            printRoutine('------------------------------------------------------')
            printRoutine(str(tweet_count))
            printRoutine(tweet)
            printRoutine(tweet_data['lang'])
            if tweet_data['lang']=='fi':
                finnishParse(tweet, tweet_count)
            result=remove_stopWords(tweet)
            translated=get_translate(' '.join(result), tweet_data['lang'])
            if translated:
                printRoutine(translated)
                get_topic(translated)
                printRoutine(get_pos(translated))
            link_extracted = extract_link(tweet)
            printRoutine(link_extracted)
            # guess_type_of(link_extracted)
            # databasePush(tweet_count, tweet_data)
            time.sleep(0.8)
    return int(tweet_count)


if __name__ == "__main__":

    translator = Translator()
    f = open("stream_results.txt", "w+")

    lda = lda_modeling()
    stop_words = set(stopwords.words('english'))
    NLP_understanding = AlchemyNLPunderstanding()

    tweet_count = 0
    tagger = geniatagger.GeniaTagger(
        '/home/moamen/work/cancer_material/geniatagger-3.0.2/geniatagger')
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()  
    db= firebase.database()

    time.sleep(7)

    for x in range(3,7):
        fread = open("outputDir/2018-03-0"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)
    f.close()
