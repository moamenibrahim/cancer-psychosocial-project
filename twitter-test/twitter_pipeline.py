import json,re
from tweets_processing import functions

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
            "kreft",
            "carcino",
            "lymphom",
            "biopsy",
            "biopsies",
            "melano",
            "sarcoma",
            "dysplasia",
            "mammogr",
            "maligna",
            "metasta",
            "PET scan",
            "ablate",
            "ablation",

        ### SPECIFIC CANCER KEYWORDS
        "bone neoplasm",
        "osteosarcoma",
        "ewing tumor",
        "fibrosarcoma",
        "histiocytoma",
        "chordoma",
        "gastrointestinal",
        "tract Cancer",
        "colorectal",
        "colon",
        "stomach adenocarcinoma",
        "lymphoma",
        "carcinoid",
        "Carcinoma",
        "breast adenocarcinoma",
        "Carcinoma in situ",
        "Sarcoma",
        "SCLC",
        "NSCLC",
        "Squamous cell carcinomas",
        "Large cell carcinomas",
        "Bronchial carcinoids",
        "lymphoma",
        "melanoma",
        "basal",
        "dermatology",
        "melanoma",
        "moles",
        "oral cavity",
        "pharynx",
        "larynx",
        "neoplasm",
        "Acoustic Neuroma",
        "Astrocytoma",
        "chordoma",
        "cNS Lymphoma",
        "craniopharyngioma",
        "medulloblastoma",
        "meningioma",
        "metastatic Brain Tumors",
        "oligodendroglioma",
        "pituitary Tumors",
        "primitive Neuroectodermal",
        "PNET",
        "schwannoma",
        "bone neoplasm",
        "osteosarcoma",
        "ewing tumor",
        "fibrosarcoma",
        "histiocytoma",
        "chordoma",
        "neuroblastoma",
        "wilms tumor",
        "osteosarcoma",
        "retinoblastoma",
        "pediatric"]


def analyze_file(fileName, tweet_count):
    """ Method to analyze file by file and calls all other methods """
    
    Named_count=0

    for line in fileName.readlines():
        tweet_data = json.loads(line)
        if("extended_tweet") in tweet_data:
            tweet = tweet_data['extended_tweet']['full_text']
        else:
            tweet = tweet_data['text']

        if any(word in tweet for word in mylist):
            tweet_count = tweet_count + 1

            # result = processing.remove_stopWords(tweet)
            # databasePush(tweet_count, tweet_data)
            
            hastags = processing.get_hashtags(tweet)
            no_links_text, links = processing.strip_links(tweet)
            # guess_type_of(links)
            pure_text = processing.strip_all_entities(no_links_text)

            # if tweet_data['lang'] == 'fi':
            #     processing.finnishParse(u"%s"%str(pure_text), tweet_count)
          
            translated = processing.get_translate(u"%s"%str(pure_text), tweet_data['lang'])
            print(translated)
            if translated:
                pos = []
<<<<<<< HEAD
                sentences = processing.segmentation(u"%s"%str(translated))
=======
                Named_count=0
                sentences = processing.segmentation(translated)
>>>>>>> 9f7ea3ff840a8dbc39bcc4a2b5d3c99da42ebfdd
                for sentence in sentences:
                    pos.append(processing.get_pos(u"%s"%str(translated)))
                dict_result = processing.check_dictionary(u"%s"%str(translated))
                hyponyms = processing.get_hyponyms(u"%s"%str(translated))
                named = processing.get_stanford_named_entity(u"%s"%str(translated))
                for i in named:
                    if ((bool( ((bool(re.search('TIME',str(i)))) or bool(re.search('LOCATION',str(i)))) or re.search('ORGANIZATION',str(i))))
                                or (bool(re.search('PERSON',str(i)))) or (bool(re.search('MONEY',str(i))))
                                or (bool(re.search('DATE',str(i))))):
                        Named_count+=1
                topic = processing.get_topic(u"%s"%str(translated))
                sentiment = processing.get_sentiment(u"%s"%str(translated))
                                
                data = {'tweet': tweet_count,
                        'lang': tweet_data['lang'], 'tweet length': len(tweet.split()),
                        'links': links, 'translation': u"%s"%str(translated), 'pos': u"%s"%str(pos),
                        'hyponyms': u"%s"%str(hyponyms), 'named entity': u"%s"%str(named),
                        'topic': topic, 'sentiment': u"%s"%str(sentiment), 'check_dictionary': dict_result,
                        'Named count': Named_count}
                
            else:
                data = {'tweet': tweet_count,
                        'lang': tweet_data['lang'], 'tweet length': len(tweet.split()),
                        'links': links}
            
            json.dumps(data, f, ensure_ascii=False)
            # f.write(u"%s"%str(data))
            # print(data)
            f.write(' \n')

    return int(tweet_count)

if __name__ == "__main__":

    processing = functions()
    f = open("stream_results.json", "w+")
    tweet_count = 0
    for x in range(3,30):
        fread = open("outputDir/2018-03-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)
    f.close()
