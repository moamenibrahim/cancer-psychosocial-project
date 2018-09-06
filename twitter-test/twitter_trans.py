import json,re,nltk
from tweets_processing import functions
from keywords_helper import cancer_keywords as cancer

def analyze_file(fileName, tweet_count):
    """ Method to analyze file by file and calls all other methods """
    
    Named_count=0

    for line in fileName.readlines():
        tweet_data = json.loads(line)
        if("extended_tweet") in tweet_data:
            tweet = tweet_data['extended_tweet']['full_text']
        else:
            tweet = tweet_data['text']

        hastags = processing.get_hashtags(tweet)
        html = 'None'
        no_links_text, links = processing.strip_links(tweet)
        if links:
            html = processing.guess_type_of(links)
        pure_text = processing.strip_all_entities(no_links_text)
    
        translated = processing.get_translate(u"%s"%str(pure_text), tweet_data['lang'])
        
        if translated:
            if (any(word.lower() in tweet for word in cancer.mylist)
                or any(stemmer.stem(word) in tweet for word in cancer.mylist)
                or any(word in hastags for word in cancer.mylist)
                ):

                tweet_count = tweet_count + 1
                print(tweet_count)

                dict_result = processing.check_dictionary(u"%s"%str(translated))
                pos = []
                sentences = processing.segmentation(u"%s"%str(translated))
                for sentence in sentences:
                    pos.append(processing.get_pos(u"%s"%str(translated)))
                hyponyms = processing.get_hyponyms(u"%s"%str(translated))
                names = processing.get_human_names(u"%s"%str(translated))
                named = processing.get_stanford_named_entity(u"%s"%str(translated))
                
                for i in named:
                    if ((bool( ((bool(re.search('TIME',str(i)))) or bool(re.search('LOCATION',str(i)))) or re.search('ORGANIZATION',str(i))))
                                or (bool(re.search('PERSON',str(i)))) or (bool(re.search('MONEY',str(i))))
                                or (bool(re.search('DATE',str(i))))):
                        Named_count+=1
                
                pure_translated = processing.remove_stopWords(u"%s"%str(translated))
                topic = processing.get_topic(u"%s"%str(pure_translated))
                # sentiment = processing.get_sentiment(u"%s"%str(pure_translated))
                sentiment = processing.RateSentiment(u"%s"%str(pure_translated))

                data = {'tweet': tweet_count,
                        'lang': tweet_data['lang'], 'tweet length': len(tweet.split()),
                        'links': links, 'translation': translated, 'pos': pos,
                        'hyponyms': hyponyms, 'named entity': named,
                        'topic': topic, 'sentiment': sentiment, 'check_dictionary': dict_result,
                        'Named count': Named_count,
                        'names':names,
                        'html':html,
                        'pure_text':pure_text}
                
                # processing.databasePush(tweet_count,data)
                json.dump(data, f, ensure_ascii=True)
                # f.write(u"%s"%str(data))
                # print(data)
                f.write(' \n')

    return int(tweet_count)

if __name__ == "__main__":

    processing = functions()
    stemmer = nltk.stem.PorterStemmer()
    f = open("stream_results_trans.json", "w+")
    tweet_count = 0
    for x in range(3,31):
        fread = open("outputDir/2018-03-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)

    for x in range(3,25):
        fread = open("outputDir/2018-06-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)

    for x in range(9,27):
        fread = open("outputDir/2018-07-"+str(x)+".json", "r")
        tweet_count=analyze_file(fread,tweet_count)

    f.close()
    if(processing.stop_firebase()==True):
        pass    
