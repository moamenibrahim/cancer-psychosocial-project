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
        "carcinoma",
        "breast adenocarcinoma",
        "carcinoma in situ",
        "sarcoma",
        "SCLC",
        "NSCLC",
        "ductal",
        "medullary",
        "phyllodes",
        "angiosarcoma",
        "mucinous",
        "colloid",
        "nipple termed Paget",
        "lobular",
        "LCIS",
        "squamous cell carcinomas",
        "large cell carcinomas",
        "bronchial carcinoids",
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
        "acoustic Neuroma",
        "astrocytoma",
        "chordoma",
        "CNS Lymphoma",
        "fibrocystic",
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
        "benign"
            ]


## From: https://www.cancer.gov/types
stomach=[
    "stomach",
    "vatsa",
    "gastric",
    "digestive",
    "gastrointestinal",
    "tract Cancer",
    "colorectal",
    "colon",
    "stomach adenocarcinoma",
    "lymphoma",
    "carcinoid"
]

breast=[
    "breast",
    "rinta",
    "carcinoma",
    "breast adenocarcinoma",
    "carcinoma in situ",
    "sarcoma",
    "BRCA1",
    "ductal",
    "medullary",
    "phyllodes",
    "angiosarcoma",
    "mucinous",
    "colloid",
    "nipple termed Paget",
    "lobular",
    "LCIS"
]

lung=[
    "lung",
    "keuhko",
    "SCLC",
    "NSCLC",
    "squamous cell carcinomas",
    "large cell carcinomas",
    "bronchial carcinoids"
]

skin=[
    "skin",
    "iho",
    "lymphoma",
    "melanoma",
    "basal",
    "dermatology",
    "melanoma",
    "moles"
]

blood=[
    "leukemia",
    "veri",
    "leucocythaemia",
    "leucocythaemias",
    "leucocythemia",
    "leucocythemia",
    "hematologic",
    "blood"
]

head_neck=[
    "neoplasm",
    "pään",
    "kaulan",
    "head",
    "neck",
    "oral cavity",
    "pharynx",
    "larynx"
]

brain=[
    "brain",
    "aviot",
    "acoustic Neuroma",
    "astrocytoma",
    "chordoma",
    "CNS Lymphoma",
    "craniopharyngioma",
    "medulloblastoma",
    "meningioma",
    "metastatic Brain Tumors",
    "oligodendroglioma",
    "pituitary Tumors",
    "primitive Neuroectodermal",
    "PNET",
    "schwannoma"
]

bone=[
    "bone",
    "luu",
    "bone neoplasm",
    "osteosarcoma",
    "ewing tumor",
    "fibrosarcoma",
    "histiocytoma",
    "chordoma"
]

pediatric=[
    "pediatric",
    "childhood",
    "child",
    "kid",
    "neuroblastoma",
    "wilms tumor",
    "osteosarcoma",
    "retinoblastoma"]

staged_list={}


def analyze_file(fileName, tweet_count):
    """ Method to analyze file by file and calls all other methods """
    for line in fileName.readlines():
        tweet_data = json.loads(line)
        if("extended_tweet") in tweet_data:
            tweet = tweet_data['extended_tweet']['full_text']
        else:
            tweet = tweet_data['text']

        if any(word.lower() in tweet for word in mylist or stemmer.stem(word) in tweet for word in mylist):
            
            tweet_count = tweet_count + 1
            
            hastags = processing.get_hashtags(tweet)
            no_links_text, links = processing.strip_links(tweet)
            pure_text = processing.strip_all_entities(no_links_text)
            # print(u"%s"%str(pure_text))
            translated = processing.get_translate(u"%s"%str(pure_text), tweet_data['lang'])
            print(tweet_count)
            
            if translated:
                tweet = u"%s"%str(translated)
            
            if any(word.lower() in tweet for word in stomach or stemmer.stem(word) in tweet for word in stomach):
        
                if ('stomach' in staged_list):
                    ## increment that topic
                    staged_list['stomach'] += 1
                else:
                    ## add topic to list
                    staged_list['stomach'] = 1  

                # staged_list_stomach_gender 
                

                # staged_list_stomach_age
                

            if any(word.lower() in tweet for word in breast or stemmer.stem(word) in tweet for word in breast):
    
                if ('breast' in staged_list):
                    ## increment that topic
                    staged_list['breast'] += 1
                else:
                    ## add topic to list
                    staged_list['breast'] = 1   

            if any(word.lower() in tweet for word in blood or stemmer.stem(word) in tweet for word in blood):
        
                if ('blood' in staged_list):
                    ## increment that topic
                    staged_list['blood'] += 1
                else:
                    ## add topic to list
                    staged_list['blood'] = 1   

            if any(word.lower() in tweet for word in lung or stemmer.stem(word) in tweet for word in lung):
    
                if ('lung' in staged_list):
                    ## increment that topic
                    staged_list['lung'] += 1
                else:
                    ## add topic to list
                    staged_list['lung'] = 1   

            if any(word.lower() in tweet for word in skin or stemmer.stem(word) in tweet for word in skin):
    
                if ('skin' in staged_list):
                    ## increment that topic
                    staged_list['skin'] += 1
                else:
                    ## add topic to list
                    staged_list['skin'] = 1   

            if any(word.lower() in tweet for word in head_neck or stemmer.stem(word) in tweet for word in head_neck):
    
                if ('head_neck' in staged_list):
                    ## increment that topic
                    staged_list['head_neck'] += 1
                else:
                    ## add topic to list
                    staged_list['head_neck'] = 1   

            if any(word.lower() in tweet for word in brain or stemmer.stem(word) in tweet for word in brain):
    
                if ('brain' in staged_list):
                    ## increment that topic
                    staged_list['brain'] += 1
                else:
                    ## add topic to list
                    staged_list['brain'] = 1   
            
            if any(word.lower() in tweet for word in bone  or stemmer.stem(word) in tweet for word in bone):
    
                if ('bone' in staged_list):
                    ## increment that topic
                    staged_list['bone'] += 1
                else:
                    ## add topic to list
                    staged_list['bone'] = 1   
            
            if any(word.lower() in tweet for word in pediatric or stemmer.stem(word) in tweet for word in pediatric):
    
                if ('pediatric' in staged_list):
                    ## increment that topic
                    staged_list['pediatric'] += 1
                else:
                    ## add topic to list
                    staged_list['pediatric'] = 1   
            
    return int(tweet_count)

if __name__ == "__main__":

    processing = functions()
    stemmer = nltk.stem.PorterStemmer()
    f = open("cancerType_results.json", "w+")
    tweet_count = 0
    for x in range(3,30):
        fread = open("outputDir/2018-03-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)
    json.dump(staged_list, f)
    f.close()