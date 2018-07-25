import json,nltk
from tweets_processing import functions
from keywords_helper import cancer_keywords

staged_list={}

def analyze_file(fileName, tweet_count):
    """ Method to analyze file by file and calls all other methods """
    print(fread)
    for line in fileName.readlines():
        try:

            tweet_data = json.loads(line)
            if("extended_tweet") in tweet_data:
                tweet = tweet_data['extended_tweet']['full_text']
            else:
                tweet = tweet_data['full_text']

            if any(word.lower() in tweet for word in mylist or stemmer.stem(word) in tweet for word in mylist):
                
                tweet_count = tweet_count + 1
                print(tweet_count)   
                json.dump(tweet_data, f)
                f.write(' \n')

        except:
            
            print("line not in json")
        
    return int(tweet_count)

if __name__ == "__main__":

    # processing = functions()
    stemmer = nltk.stem.PorterStemmer()
    f = open("search_dir/head_neck_tweets_filter.json", "w+")
    tweet_count = 0
    fread = open("search_dir/head_neck_tweets.json", "r")
    tweet_count=analyze_file(fread,tweet_count)
    f.close()