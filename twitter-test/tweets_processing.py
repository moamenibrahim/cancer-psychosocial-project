import os 
import sys 
import json
import re
import geniatagger
import string
import time
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from lda_topic import lda_modeling
from ibmNLPunderstanding import AlchemyNLPunderstanding
from googletrans import Translator

translator = Translator()

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
            "Malignant",  # Refers to a tumor that is cancerous
            "metastasis", # Cancer spreading
            "oncology",   # Study of cancer 
            "oncologist",
            "pathologist",
            # Refers to cells that have the potential to become cancerous.
            "precancerous",
            # A cancer that develops in the tissues that support and connect the body, such as fat and muscle.
            "Sarcoma",
            "telemedicine",
            "healthcare",
            "chemotherapy",
            "mammogram"]

family_list = [ "family",
                "sad",
                "love",
                "hate",
                "father",
                "son",
                "daughter",
                "mother"]

friend_list =["friends",
              "friendship"]
              
money_list =["money",
             "price"]


lda = lda_modeling()

stop_words = set(stopwords.words('english'))

NLP_understanding = AlchemyNLPunderstanding()

def remove_stopWords(tweet):
    norm = []
    exclude = set(string.punctuation)
    word_tokens = word_tokenize(tweet)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    punc_free = ' '.join(ch for ch in filtered_sentence if ch not in exclude)
    print(punc_free)
    return filtered_sentence

    # stopwords_file = open("./finnish_stopwords.txt", "r")
	# lines = stopwords_file.read().split(",")
	# stopwords = lines[0].split("\n")
	# tokenizer = RegexpTokenizer(r'\w+')
	# texts = []
	# for doc in docs:
	# 	raw = doc.decode().lower()
	# 	tokens = tokenizer.tokenize(raw)
	# 	stopped_tokens = [i for i in tokens if not i in stopwords and len(i) != 1]
	# 	texts.append(stopped_tokens)

def get_topic(input_str):
    try:
        topic = lda.generate_topic(input_str)
        if any(word in topic for word in family_list):
            print("family related tweet: extracting emotions")
            get_sentiment(input_str)
        
        if any(word in topic for word in friend_list):
            print("friend related tweet: extracting emotions")
            get_sentiment(input_str)

        if any(word in topic for word in money_list):
            print("money related tweet")
            get_sentiment(input_str)
        return True
    except:
        print("Error getting topic")
    

def get_translate(input_str,lang):
    if(lang!='und'):
        translated=translator.translate(input_str, dest='en', src=lang)
        print(translated)
        return translated.text

def get_pos(tweet):
    out = tagger.parse(tweet)
    print(out)

def get_sentiment(input_str):
    NLP_understanding.get_response(input_str)

def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

def analyze_file(fileName, tweet_count):
    for line in fileName.readlines():
        tweet_data = json.loads(line)
        if("extended_tweet") in tweet_data:
            tweet = tweet_data['extended_tweet']['full_text']
            if any(word in tweet for word in mylist):
                tweet_count = tweet_count + 1
                print(tweet_count)
                print(tweet)
                print(tweet_data['lang'])
                result=remove_stopWords(tweet)
                try:
                    translated=get_translate(' '.join(result), tweet_data['lang'])
                    pass
                except:
                    print("Failed to translate text")
                    pass

                get_topic(translated)
                time.sleep(0.8)
            
        else:
            tweet = tweet_data['text']
            if any(word in tweet for word in mylist):
                tweet_count = tweet_count + 1
                print(tweet_count)
                print(tweet)
                print(tweet_data['lang'])
                result= remove_stopWords(tweet)
                try:
                    translated=get_translate(' '.join(result), tweet_data['lang'])
                except:
                    print("Failed to translate text")
                
                get_topic(translated)
                time.sleep(0.8)


if __name__ == "__main__":
    tweet_count = 0
    tagger = geniatagger.GeniaTagger(
        '/home/moamen/work/cancer_material/geniatagger-3.0.2/geniatagger')
    time.sleep(7)
    for x in range(3,7):
        fread = open("outputDir/2018-03-0"+str(x)+".json", "r")
        analyze_file(fread,tweet_count)
