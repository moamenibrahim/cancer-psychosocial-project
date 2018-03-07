import os 
import sys 
import json
import geniatagger
import time
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from lda_topic import lda_modeling
from ibmNLPunderstanding import AlchemyNLPunderstanding

fwrite = open("output.txt","w+")

mylist = [  "cancer",
            "Tumor",
            "Leukemia",
            "Neuroblastoma",
            "Paraganglioma",
            "Retinoblastoma",
            "Astrocytomas",
            "Retinoblastoma",
            "Lymphoma",
            "Melanoma",
            "syöpä",
            "kasvain",
            "säteily",
            "hoito",
            "kuolla",
            "Cancer",
            "Malignant",  # Refers to a tumor that is cancerous
            "Metastasis", # Cancer spreading
            "Oncology",   # Study of cancer 
            "Oncologist",
            "Pathologist",
            # Refers to cells that have the potential to become cancerous.
            "Precancerous",
            # A cancer that develops in the tissues that support and connect the body, such as fat and muscle.
            "Sarcoma"]

family_list = [ "family",
                "sad",
                "love",
                "hate"]

lda = lda_modeling()

stop_words = set(stopwords.words('english'))

NLP_understanding = AlchemyNLPunderstanding()

def remove_stopWords(tweet):
    word_tokens = word_tokenize(tweet)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    print(filtered_sentence) 
    fwrite.write(str(filtered_sentence))
    return filtered_sentence

def get_topic(input_str):
    with open("input.txt", "a") as file:
        file.write(input_str+"\n")
    topic = lda.generate_topic()
    print(topic)
    if any(word in topic for word in family_list):
        get_sentiment(input_str)

def get_pos(tweet):
    out = tagger.parse(tweet)
    print(out)
    fwrite.write(str(out)+'\n')

def get_sentiment(input_str):
    NLP_understanding.get_response(input_str)

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
                get_topic(''.join(result))
            
        else:
            tweet = tweet_data['text']
            if any(word in tweet for word in mylist):
                tweet_count = tweet_count + 1
                print(tweet_count)
                print(tweet)
                print(tweet_data['lang'])
                result= remove_stopWords(tweet)
                get_topic(''.join(result))


if __name__ == "__main__":
    tweet_count = 0
    tagger = geniatagger.GeniaTagger(
        '/home/moamen/work/cancer_project/geniatagger-3.0.2/geniatagger')
    time.sleep(6.5)
    for x in range(3,6):
        fread = open("outputDir/2018-03-0"+str(x)+".json", "r")
        analyze_file(fread,tweet_count)
