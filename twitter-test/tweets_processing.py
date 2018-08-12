import os 
import sys 
import json
import re
import operator
import geniatagger
import string
import pyrebase
import urllib
import mimetypes
import subprocess
import nltk 
import time
import enchant
import shlex
import threading
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from lda_topic import lda_modeling
from googletrans import Translator
from nltk.corpus import wordnet as wn
from nltk.tokenize import RegexpTokenizer
from os.path import expanduser
from nltk.tag import StanfordNERTagger
sys.path.insert(0, '../IBM')
from ibmNLPunderstanding import AlchemyNLPunderstanding
from nameparser.parser import HumanName



""" Configuration for the firbase database settings """ 
config = { 
    "apiKey": "AIzaSyBIJYd5Xxa7DIORsLPJUCT2r4DqUa_bxlo",
    "authDomain": "analysis-820dc.firebaseapp.com",
    "databaseURL": "https://analysis-820dc.firebaseio.com",
    "projectId": "analysis-820dc",
    "storageBucket": "analysis-820dc.appspot.com",
    "messagingSenderId": "863565878024",
    "serviceAccount": "../../cancerDashboard/key.json"
} 

class functions(object):
    def __init__(self):
        self.translator = Translator()
        self.lda = lda_modeling()
        self.stop_words = set(stopwords.words('english'))
        self.NLP_understanding = AlchemyNLPunderstanding()
        # self.tagger = geniatagger.GeniaTagger(
        #     '../../cancer/geniatagger-3.0.2/geniatagger')
        self.dictionary= enchant.Dict("en_US")
        self.reauthorize_firebase()
        self.th=threading.Timer(60*30, self.reauthorize_firebase)
        self.th.start()
        time.sleep(3)

    def segmentation(self, tweet):
        """Dividing tweets to sentences for analysis"""
        return nltk.sent_tokenize(tweet)
        

    def get_hashtags(self, tweet):
        """ Extracting Hashtags from tweets or text """
        entity_prefixes = '#'
        words = []
        for word in tweet.split():
            word = word.strip()
            if word:
                if word[0] in entity_prefixes:
                    words.append(word)
        return ' '.join(words)


    def get_link(self, tweet):
        """ Extracting links from tweets or text """
        regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        match = re.search(regex, tweet)
        if match:
            return match.group()
        return ''


    def strip_links(self, text):
        """Extracts links from tweets and returns it"""
        link_regex = re.compile(
            '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links = re.findall(link_regex, text)
        for link in links:
            text = text.replace(link[0], ' ')
        return text, links


    def strip_all_entities(self, text):
        """Extracts mentions and hashtags from tweets and returns it"""
        entity_prefixes = ['@', '#']
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)


    def get_pos(self, tweet):
        """ 
        part of speech tagging extraction
        """
        staged_rows = {}
        staged_nouns = {}
        staged_verbs = {}
        staged_determiner = {}
        staged_adjective = {}
        staged_pronoun = {}
        staged_adverb = {}
        staged_number = {}

        text = word_tokenize(str(tweet))
        result_postag = nltk.pos_tag(text)
        for row in result_postag:
            if (row[1] != ''):
                if (row[1] in staged_rows):
                    ## increment
                    staged_rows[row[1]] += 1
                else:
                    ## add to list
                    staged_rows[row[1]] = 1

        staged_rows = sorted(staged_rows.items(),
                            key=operator.itemgetter(1), reverse=True)
        return staged_rows


    def get_stanford_pos(self, tweet):
        """
        part of speech tagging extraction
        """
        path_to_model ='../../cancer/stanford/stanford-postagger/models/english-bidirectional-distsim.tagger'
        path_to_jar ='../../cancer/stanford/stanford-postagger/stanford-postagger.jar'
        st = StanfordPOSTagger(path_to_model, path_to_jar=path_to_jar)
        result = st.tag(tweet.split())
        return result


    def get_hyponyms(self,tweet):
        """ 
        hyponyms extraction and checking the topics list 
        """
        entities = {}
        words = tweet.split()
        for word in words:
            for i, syn in enumerate(wn.synsets(word)):
                if(i>3):
                    pass
                else:
                    entities["Hyponyms"] = []
                    for hyponym in syn.hyponyms():
                        for lemma in hyponym.lemmas():
                            entities["Hyponyms"].append(lemma.name())
        return entities

    def get_stanford_named_entity(self, tweet):
        """ 
        get named entity recognition and check if words have entry in lexical database 
        """
        stanford_dir = '../../cancer/stanford/stanford-nertagger/'
        jarfile = stanford_dir + 'stanford-ner.jar'
        modelfile = stanford_dir + 'classifiers/english.muc.7class.distsim.crf.ser.gz'
        st = StanfordNERTagger(model_filename=modelfile, path_to_jar=jarfile)
        result = st.tag(tweet.split())
        return result


    def remove_stopWords(self, tweet):
        """ Removing english stop words from the text sent 
        including punctuations 
        """
        exclude = set(string.punctuation)
        word_tokens = word_tokenize(tweet)
        filtered_sentence = [w for w in word_tokens if not w in self.stop_words]
        punc_free = ' '.join(ch for ch in filtered_sentence if ch not in exclude)
        return filtered_sentence

    def call_train_lda(self, location):
        """
        Train Topic extraction from text using LDA (Latent Dirichet Allocation): 
        """
        try:
            self.lda.train_lda(location)
        except:
            print("Failed to train topic classifier")

    def get_topic(self, input_str):
        """ 
        Topic extraction from text using LDA (Latent Dirichet Allocation): 
        It classifies the text according to whether it is family, friend, money related
        """
        try:
            topic = self.lda.generate_topic(input_str)
            return topic

        except:
            print("Failed to get topic")
            return False


    def get_translate(self, input_str, lang):
        """ using googletrans to translate text from any language to English """
        if(lang!='und'):
            try:
                translated=self.translator.translate(input_str, dest='en', src=lang)
                return translated.text
            except:
                # print("Failed to translate text")
                return False


    # def get_Geniapos(self, tweet):
    #     """ Genia Tagger part of speech tagging extraction
    #     Medical part of speech tagger """
    #     out = self.tagger.parse(tweet)
    #     return out


    def get_sentiment(self, input_str):
        """ Get sentiment analysis when needed, the used API is IBM watson's """
        return self.NLP_understanding.get_response(input_str)


    def extract_link(self, text):
        """ Extracting links from tweets or text """
        regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        match = re.search(regex, text)
        if match:
            return match.group()
        return ''


    def guess_type_of(self, link, strict=True):
        """ Determine the link info and know whether it can be helpful for
        the study or no """
        # print(link[0][0])
        link_type, _ = mimetypes.guess_type(str(link[0][0]))
        return link_type


    def databasePush(self, tweet_count, tweet_data):
        """ A method to send tweets without processed data 
        to the database on firebase """
        self.db.child("Twitter").child("tweet"+str(tweet_count))
        self.db.set(tweet_data)
        return

    def reauthorize_firebase(self):
        """A method to re-authorize access to firebase 
        every one hour"""
        print("authorizing access to firebase")
        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.th=threading.Timer(60*30, self.reauthorize_firebase)
        self.th.start()
        return

    def stop_firebase(self):
        """Cancelling the thread responsible for 
        re-authorize access to firebase"""
        self.th.cancel()
        while(self.th.is_alive):
            self.th.cancel()
        return True

    ''' Finnish functions part '''
    def finnishParse(self, tweet, tweet_count):
        """ Parsing Finnish words and text, the library was developed by 
        univerity of Turku, it performs sentence splitting, tokenization, tagging, parsing """
            
        wd = os.getcwd()
        os.chdir("../../cancer/Finnish-dep-parser")
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


    def remove_finnstopWords(self, tweet):
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


    ''' Fetching information about users (tweeps) '''
    def analyze_location(self, fileName):
        """ Method to analyze file by file and calls all other methods """
        staged_location = {}
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


    def analyze_user(self, fileName):
        """ Method to analyze file by file and calls all other methods """
        staged_users = {}
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

    def check_dictionary(self, tweet):
        """Making sure that the translated text is in dictionary 
        to verify the translation of tweets"""
        in_dict=0
        not_in_dict=0
        text = word_tokenize(str(tweet))
        for word in text:
            result = self.dictionary.check(word)
            if result == True:
                in_dict +=1
            else:
                not_in_dict +=1 
        return in_dict/(in_dict+not_in_dict)

    def get_human_names(self,text):
        """Catching human names from tweets"""
        tokens = nltk.tokenize.word_tokenize(text)
        pos = nltk.pos_tag(tokens)
        sentt = nltk.ne_chunk(pos, binary = False)
        person_list = []
        person = []
        name = ""
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1: #avoid grabbing lone surnames
                for part in person:
                    name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []
        return (person_list)

    def RateSentiment(self,sentiString):
        """Senti Strength java software to get sentiment from tweets"""
        #open a subprocess using shlex to get the command line string into the correct args list format
        p = subprocess.Popen(shlex.split("java -jar ../../cancer/SentiStrength.jar stdin explain sentidata ../../cancer/SentiStrength_Data/"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #communicate via stdin the string to be rated. Note that all spaces are replaced with +
        stdout_text, stderr_text = p.communicate(sentiString.replace(" ","+").encode("utf-8"))
        #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
        stdout_text = stdout_text.decode("utf-8").rstrip().replace("\t","")
        return stdout_text[0],stdout_text[1:3]