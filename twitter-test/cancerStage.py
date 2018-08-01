import json,nltk,re
from tweets_processing import functions
from keywords_helper import stages_keywords as stage
from keywords_helper import cancer_keywords as cancer

staged_list={}
staged_TMN_list={}

def analyze_file(fileName, tweet_count):
    """ Method to analyze file by file and calls all other methods """
    for line in fileName.readlines():
        tweet_data = json.loads(line)
        if("extended_tweet") in tweet_data:
            tweet = tweet_data['extended_tweet']['full_text']
        else:
            tweet = tweet_data['text']

        hastags = processing.get_hashtags(tweet)
        # print(hastags)

        if (any(word.lower() in tweet for word in cancer.mylist)
                or any(stemmer.stem(word) in tweet for word in cancer.mylist)
                or any(word in hastags for word in cancer.mylist)):
            
            tweet_count = tweet_count + 1
            
            no_links_text, links = processing.strip_links(tweet)
            pure_text = processing.strip_all_entities(no_links_text)
            translated = processing.get_translate(u"%s"%str(pure_text), tweet_data['lang'])
            print(tweet_count)

            if translated:
                tweet = u"%s"%str(translated)
            
            if (any(word.lower() in tweet for word in stage.stage_0)
                    or any(stemmer.stem(word) in tweet for word in stage.stage_0)
                    or any(word in hastags for word in stage.stage_0)):
                
                if ('stage_0' in staged_list):
                        ## increment that topic
                    staged_list['stage_0'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_0'] = 1  
                
            if (any(word.lower() in tweet for word in stage.stage_1)
                    or  any(stemmer.stem(word) in tweet for word in stage.stage_1)
                    or  any(word in hastags for word in stage.stage_1)):
                
                if ('stage_1' in staged_list):
                        ## increment that topic
                    staged_list['stage_1'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_1'] = 1  

            if (any(word.lower() in tweet for word in stage.stage_2)
                    or  any(stemmer.stem(word) in tweet for word in stage.stage_2)
                    or  any(word in hastags for word in stage.stage_2)):
                
                if ('stage_2' in staged_list):
                        ## increment that topic
                    staged_list['stage_2'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_2'] = 1  

            if (any(word.lower() in tweet for word in stage.stage_3 )
                    or  any(stemmer.stem(word) in tweet for word in stage.stage_3)
                    or  any(word in hastags for word in stage.stage_3)):
                
                if ('stage_3' in staged_list):
                        ## increment that topic
                    staged_list['stage_3'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_3'] = 1  

            if (any(word.lower() in tweet for word in stage.stage_4 )
                    or  any(stemmer.stem(word) in tweet for word in stage.stage_4)
                    or  any(word in hastags for word in stage.stage_4)):
                
                if ('stage_4' in staged_list):
                        ## increment that topic
                    staged_list['stage_4'] += 1
                else:
                    ## add topic to list
                    staged_list['stage_4'] = 1  


            # TNM Match 
            match=re.findall(r'[T]+[1-4]',tweet)
            if match:
                for i in match: 
                    if (i in staged_TMN_list):
                        ## increment that topic
                        staged_TMN_list[i] += 1
                    else:
                        ## add topic to list
                        staged_TMN_list[i] = 1  

            match=re.findall(r'[N]+[1-4]',tweet)
            if match:
                for i in match: 
                    if (i in staged_TMN_list):
                        ## increment that topic
                        staged_TMN_list[i] += 1
                    else:
                        ## add topic to list
                        staged_TMN_list[i] = 1

            match=re.findall(r'[M]+[1-4]',tweet)
            if match:
                for i in match: 
                    if (i in staged_TMN_list):
                        ## increment that topic
                        staged_TMN_list[i] += 1
                    else:
                        ## add topic to list
                        staged_TMN_list[i] = 1 
            
    return int(tweet_count)

if __name__ == "__main__":

    processing = functions()
    stemmer = nltk.stem.PorterStemmer()
    f = open("cancerStage_results.json", "w+")
    tweet_count = 0
    for x in range(3,30):
        fread = open("outputDir/2018-03-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)

    for x in range(3,24):
        fread = open("outputDir/2018-06-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)

    for x in range(9,26):
        fread = open("outputDir/2018-07-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)

    json.dump(staged_list, f)
    json.dump(staged_TMN_list, f)
    
    processing.stop_firebase()
    f.close()