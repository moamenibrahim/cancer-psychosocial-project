import json
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
            "kreft"]


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

            if tweet_data['lang'] == 'fi':
                processing.finnishParse(tweet, tweet_count)
            
            # result = processing.remove_stopWords(tweet)
            # link_extracted = processing.extract_link(tweet)
            # guess_type_of(link_extracted)
            # databasePush(tweet_count, tweet_data)

            no_links_text, links = processing.strip_links(tweet)
            pure_text = processing.strip_all_entities(no_links_text)
            translated = processing.get_translate(pure_text, tweet_data['lang'])

            if translated:
                pos = processing.get_pos(translated)
                hyponyms = processing.get_hyponyms(translated)
                named = processing.get_stanford_named_entity(translated)
                topic = processing.get_topic(translated)
                sentiment = processing.get_sentiment(translated)
                
                data = {'tweet': tweet_count,
                        'lang': tweet_data['lang'], 'tweet length': len(tweet.split()),
                        'links': links, 'translation': translated, 'pos': pos,
                        'hyponyms': hyponyms, 'named entity': named,
                        'topic': topic, 'sentiment': sentiment}
                
            else:
                data = {'tweet': tweet_count,
                        'lang': tweet_data['lang'], 'tweet length': len(tweet.split()),
                        'links': links}
            
            json.dump(data, f)
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
