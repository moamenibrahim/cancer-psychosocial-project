import json,nltk
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
            "malignant",  
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
            "sarcoma",
            "telemedicine",
            "healthcare",
            "chemotherapy",
            "radiation",
            "hormone therapy",
            "mammogram",
            "kræft",
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
        "pediatric",
        "XRCC1",
        "EGFR",
        "KRas",
        "P53",
        "BRCA1",
        "benign"]

stage_0 = [
    "benign",
    "stage 0",
    "zero",
    "stage zero",
    "situ"
]

stage_1 = [
    "stage 1",
    "stage I",
    "first stage",
    "regional"
]
stage_2 = [
    "stage 2",
    "stage II",
    "second stage",
    "regional"
]
stage_3 = [
    "stage 3",
    "stage III",
    "third stage",
    "regional"
]
stage_4 = [
    "stage 4",
    "stage IV",
    "fourth stage",
    "distant"
]

TNM = []

staged_list={}

def analyze_file(fileName, tweet_count):
    """ Method to analyze file by file and calls all other methods """
    for line in fileName.readlines():
        tweet_data = json.loads(line)
        if("extended_tweet") in tweet_data:
            tweet = tweet_data['extended_tweet']['full_text']
        else:
            tweet = tweet_data['text']

        hastags = processing.get_hashtags(tweet)

        if any(word.lower() in tweet for word in mylist 
                or stemmer.stem(word) in tweet for word in mylist 
                or word.lower() in hastags for word in mylist):
            
            tweet_count = tweet_count + 1
            
            no_links_text, links = processing.strip_links(tweet)
            pure_text = processing.strip_all_entities(no_links_text)
            # print(u"%s"%str(pure_text))
            translated = processing.get_translate(u"%s"%str(pure_text), tweet_data['lang'])
            print(tweet_count)

            if translated:
                tweet = u"%s"%str(translated)
            
            if any(word.lower() in tweet for word in stage_0 
                    or stemmer.stem(word) in tweet for word in stage_0
                    or word.lower() in hastags for word in stage_0):
                
                if ('stage_0' in staged_list):
                        ## increment that topic
                    staged_list['stage_0'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_0'] = 1  
                
            if any(word.lower() in tweet for word in stage_1 
                    or stemmer.stem(word) in tweet for word in stage_1
                    or word.lower() in hastags for word in stage_1):
                
                if ('stage_1' in staged_list):
                        ## increment that topic
                    staged_list['stage_1'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_1'] = 1  

            if any(word.lower() in tweet for word in stage_2 
                    or stemmer.stem(word) in tweet for word in stage_2
                    or word.lower() in hastags for word in stage_2):
                
                if ('stage_2' in staged_list):
                        ## increment that topic
                    staged_list['stage_2'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_2'] = 1  

            if any(word.lower() in tweet for word in stage_3 
                    or stemmer.stem(word) in tweet for word in stage_3
                    or word.lower() in hastags for word in stage_3):
                
                if ('stage_3' in staged_list):
                        ## increment that topic
                    staged_list['stage_3'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_3'] = 1  

            if any(word.lower() in tweet for word in stage_4 
                    or stemmer.stem(word) in tweet for word in stage_4
                    or word.lower() in hastags for word in stage_4):
                
                if ('stage_4' in staged_list):
                        ## increment that topic
                    staged_list['stage_4'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_4'] = 1  
            
    return int(tweet_count)

if __name__ == "__main__":

    processing = functions()
    stemmer = nltk.stem.PorterStemmer()
    f = open("cancerStage_results.json", "w+")
    tweet_count = 0
    for x in range(3,30):
        fread = open("outputDir/2018-03-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)
    json.dump(staged_list, f)
    f.close()