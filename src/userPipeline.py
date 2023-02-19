import json
import re
from tweets_processing import functions


def analyze_file(fileName, tweet_count):
    """ Method to analyze file by file and calls all other methods """

    for line in fileName.readlines():
        tweet_count = tweet_count + 1
        print(tweet_count)

        # tweet=line
        tweet_data = json.loads(line)
        if("extended_tweet") in tweet_data:
            tweet = tweet_data['extended_tweet']['full_text']
        else:
            tweet = tweet_data['text']

        hastags = processing.get_hashtags(tweet)
        no_links_text, links = processing.strip_links(tweet)
        pure_text = processing.strip_all_entities(no_links_text)

        # Check if it is the end of the tweet (so tweet is a link only)
        if(len(pure_text) == 0):
            print('Tweet is only a link, no pure text')
            pass
        else:
            pos = []
            Named_count = 0
            sentences = processing.segmentation(u"%s" % str(pure_text))
            for sentence in sentences:
                pos.append(processing.get_pos(sentence))
            dict_result = processing.check_dictionary(u"%s" % str(pure_text))
            hyponyms = processing.get_hyponyms(u"%s" % str(pure_text))
            named = processing.get_stanford_named_entity(
                u"%s" % str(pure_text))
            for i in named:
                if ((bool(((bool(re.search('TIME', str(i)))) or bool(re.search('LOCATION', str(i)))) or re.search('ORGANIZATION', str(i))))
                    or (bool(re.search('PERSON', str(i)))) or (bool(re.search('MONEY', str(i))))
                        or (bool(re.search('DATE', str(i))))):
                    Named_count += 1
            topic = processing.get_topic(u"%s" % str(pure_text))
            # sentiment = processing.get_sentiment(pure_text)
            sentiment = processing.RateSentiment(u"%s" % str(pure_text))

            data = {'tweet': tweet_count,
                    'tweet length': len(tweet.split()),
                    'links': links, 'pure_text': u"%s" % str(pure_text), 'pos': pos,
                    'hyponyms': hyponyms, 'named entity': named,
                    'topic': topic, 'sentiment': sentiment,
                    'check_dictionary': dict_result,
                    'Named Count': Named_count}

            json.dump(data, f)
            f.write(' \n')

    return int(tweet_count)


if __name__ == "__main__":

    processing = functions()
    for x in range(2014, 2019):
        tweet_count = 0
        f = open("time_div/results/user_results_"+str(x)+".json", "w+")
        fread = open("time_div/years/user_results_"+str(x)+".json", "r")
        tweet_count = analyze_file(fread, tweet_count)
        f.close()
        fread.close()
    print("Done")
    if(processing.stop_firebase() == True):
        pass
