import json
import nltk
from tweets_processing import functions
from chicksexer import predict_gender
from collections import Counter
from keywords_helper import ages_keywords as age
from keywords_helper import cancer_keywords as cancer
from keywords_helper import gender_keywords as gender

staged_age_stomach = {}
staged_age_breast = {}
staged_age_skin = {}
staged_age_bone = {}
staged_age_pediatric = {}
staged_age_brain = {}
staged_age_head_neck = {}
staged_age_blood = {}
staged_age_lung = {}

staged_list_stomach = {"male": 0, "female": 0}
staged_list_breast = {"male": 0, "female": 0}
staged_list_skin = {"male": 0, "female": 0}
staged_list_bone = {"male": 0, "female": 0}
staged_list_pediatric = {"male": 0, "female": 0}
staged_list_brain = {"male": 0, "female": 0}
staged_list_head_neck = {"male": 0, "female": 0}
staged_list_blood = {"male": 0, "female": 0}
staged_list_lung = {"male": 0, "female": 0}

staged_list = {}
staged_gender_total = []


def analyze_file(fileName, tweet_count):
    """ Method to analyze file by file and calls all other methods """
    for line in fileName.readlines():
        tweet_data = json.loads(line)
        if("extended_tweet") in tweet_data:
            tweet = tweet_data['extended_tweet']['full_text']
        else:
            tweet = tweet_data['text']
        hastags = processing.get_hashtags(tweet)

        if (any(word.lower() in tweet for word in cancer.mylist)
                or any(stemmer.stem(word) in tweet for word in cancer.mylist)
                or any(word in hastags for word in cancer.mylist)):

            tweet_count = tweet_count + 1
            no_links_text, links = processing.strip_links(tweet)
            pure_text = processing.strip_all_entities(no_links_text)
            translated = processing.get_translate(
                u"%s" % str(pure_text), tweet_data['lang'])
            print(tweet_count)
            if translated:
                tweet = u"%s" % str(translated)
            sentences = [[word.lower() for word in nltk.word_tokenize(sentence)]
                         for sentence in nltk.sent_tokenize(tweet)]
            sents, words = count_gender(sentences)
            total = sum(words.values())
            for gender, count in words.items():
                pcent = (count / total) * 100
                nsents = sents[gender]
                staged_gender_total.append(
                    {'tweet_count': tweet_count, 'pcent': pcent, 'nsents': nsents})

            if (any(word.lower() in tweet for word in cancer.stomach)
                or any(stemmer.stem(word) in tweet for word in cancer.stomach)
                    or any(word in hastags for word in cancer.stomach)):

                if ('stomach' in staged_list):
                    # increment that topic
                    staged_list['stomach'] += 1
                else:
                    # add topic to list
                    staged_list['stomach'] = 1

                detect_age(tweet, 'stomach')
                result = prepare_username(
                    name=tweet_data['user']['name'].encode('ascii', 'ignore'))

                if result['male'] > result['female']:
                    staged_list_stomach['male'] += 1
                else:
                    staged_list_stomach['female'] += 1

            if (any(word.lower() in tweet for word in cancer.breast)
                or any(stemmer.stem(word) in tweet for word in cancer.breast)
                    or any(word in hastags for word in cancer.breast)):

                if ('breast' in staged_list):
                    # increment that topic
                    staged_list['breast'] += 1
                else:
                    # add topic to list
                    staged_list['breast'] = 1

                detect_age(tweet, 'breast')
                result = prepare_username(
                    name=tweet_data['user']['name'].encode('ascii', 'ignore'))

                if result['male'] > result['female']:
                    staged_list_breast['male'] += 1
                else:
                    staged_list_breast['female'] += 1

            if (any(word.lower() in tweet for word in cancer.blood)
                or any(stemmer.stem(word) in tweet for word in cancer.blood)
                    or any(word in hastags for word in cancer.blood)):

                if ('blood' in staged_list):
                    # increment that topic
                    staged_list['blood'] += 1
                else:
                    # add topic to list
                    staged_list['blood'] = 1

                detect_age(tweet, 'blood')
                result = prepare_username(
                    name=tweet_data['user']['name'].encode('ascii', 'ignore'))

                if result['male'] > result['female']:
                    staged_list_blood['male'] += 1
                else:
                    staged_list_blood['female'] += 1

            if (any(word.lower() in tweet for word in cancer.lung)
                or any(stemmer.stem(word) in tweet for word in cancer.lung)
                    or any(word in hastags for word in cancer.lung)):

                if ('lung' in staged_list):
                    # increment that topic
                    staged_list['lung'] += 1
                else:
                    # add topic to list
                    staged_list['lung'] = 1

                detect_age(tweet, 'lung')
                result = prepare_username(
                    name=tweet_data['user']['name'].encode('ascii', 'ignore'))

                if result['male'] > result['female']:
                    staged_list_lung['male'] += 1
                else:
                    staged_list_lung['female'] += 1

            if (any(word.lower() in tweet for word in cancer.skin)
                or any(stemmer.stem(word) in tweet for word in cancer.skin)
                    or any(word in hastags for word in cancer.skin)):

                if ('skin' in staged_list):
                    # increment that topic
                    staged_list['skin'] += 1
                else:
                    # add topic to list
                    staged_list['skin'] = 1

                detect_age(tweet, 'skin')
                result = prepare_username(
                    name=tweet_data['user']['name'].encode('ascii', 'ignore'))

                if result['male'] > result['female']:
                    staged_list_skin['male'] += 1
                else:
                    staged_list_skin['female'] += 1

            if (any(word.lower() in tweet for word in cancer.head_neck)
                or any(stemmer.stem(word) in tweet for word in cancer.head_neck)
                    or any(word in hastags for word in cancer.head_neck)):

                if ('head_neck' in staged_list):
                    # increment that topic
                    staged_list['head_neck'] += 1
                else:
                    # add topic to list
                    staged_list['head_neck'] = 1

                detect_age(tweet, 'head_neck')
                result = prepare_username(
                    name=tweet_data['user']['name'].encode('ascii', 'ignore'))

                if result['male'] > result['female']:
                    staged_list_head_neck['male'] += 1
                else:
                    staged_list_head_neck['female'] += 1

            if (any(word.lower() in tweet for word in cancer.brain)
                or any(stemmer.stem(word) in tweet for word in cancer.brain)
                    or any(word in hastags for word in cancer.brain)):

                if ('brain' in staged_list):
                    # increment that topic
                    staged_list['brain'] += 1
                else:
                    # add topic to list
                    staged_list['brain'] = 1

                detect_age(tweet, 'brain')
                result = prepare_username(
                    name=tweet_data['user']['name'].encode('ascii', 'ignore'))

                if result['male'] > result['female']:
                    staged_list_brain['male'] += 1
                else:
                    staged_list_brain['female'] += 1

            if (any(word.lower() in tweet for word in cancer.bone)
                or any(stemmer.stem(word) in tweet for word in cancer.bone)
                    or any(word in hastags for word in cancer.bone)):

                if ('bone' in staged_list):
                    # increment that topic
                    staged_list['bone'] += 1
                else:
                    # add topic to list
                    staged_list['bone'] = 1

                detect_age(tweet, 'bone')
                result = prepare_username(
                    name=tweet_data['user']['name'].encode('ascii', 'ignore'))

                if result['male'] > result['female']:
                    staged_list_bone['male'] += 1
                else:
                    staged_list_bone['female'] += 1

            if (any(word.lower() in tweet for word in cancer.pediatric)
                or any(stemmer.stem(word) in tweet for word in cancer.pediatric)
                    or any(word in hastags for word in cancer.pediatric)):

                if ('pediatric' in staged_list):
                    # increment that topic
                    staged_list['pediatric'] += 1
                else:
                    # add topic to list
                    staged_list['pediatric'] = 1

                detect_age(tweet, 'pediatric')
                result = prepare_username(
                    name=tweet_data['user']['name'].encode('ascii', 'ignore'))

                if result['male'] > result['female']:
                    staged_list_pediatric['male'] += 1
                else:
                    staged_list_pediatric['female'] += 1

    return int(tweet_count)


def genderize(words):

    mwlen = len(gender.MALE_WORDS.intersection(words))
    fwlen = len(gender.FEMALE_WORDS.intersection(words))
    if mwlen > 0 and fwlen == 0:
        return gender.MALE
    elif mwlen == 0 and fwlen > 0:
        return gender.FEMALE
    elif mwlen > 0 and fwlen > 0:
        return gender.BOTH
    else:
        return gender.UNKNOWN


def count_gender(sentences):

    sents = Counter()
    words = Counter()
    for sentence in sentences:
        gender = genderize(sentence)
        sents[gender] += 1
        words[gender] += len(sentence)
    return sents, words


def detect_age(text, cancer_type):

    list_name = 'staged_age_%s' % cancer_type
    print(list_name)
    if (any(word.lower() in text for word in age.set_13_18) or any(stemmer.stem(word) in text for word in age.set_13_18)):
        if ('set_13_18' in eval(list_name)):
            # increment that topic
            eval(list_name)['set_13_18'] += 1
        else:
            # add topic to list
            eval(list_name)['set_13_18'] = 1

    if (any(word.lower() in text for word in age.set_19_22) or any(stemmer.stem(word) in text for word in age.set_19_22)):
        if ('set_19_22' in eval(list_name)):
            # increment that topic
            eval(list_name)['set_19_22'] += 1
        else:
            # add topic to list
            eval(list_name)['set_19_22'] = 1

    if (any(word.lower() in text for word in age.set_23_29) or any(stemmer.stem(word) in text for word in age.set_23_29)):
        if ('set_23_29' in eval(list_name)):
            # increment that topic
            eval(list_name)['set_23_29'] += 1
        else:
            # add topic to list
            eval(list_name)['set_23_29'] = 1

    if (any(word.lower() in text for word in age.set_30_65) or any(stemmer.stem(word) in text for word in age.set_30_65)):
        if ('set_30_65' in eval(list_name)):
            # increment that topic
            eval(list_name)['set_30_65'] += 1
        else:
            # add topic to list
            eval(list_name)['set_30_65'] = 1


def prepare_username(name):

    # Filtering unknown characters
    result = name.decode("utf-8")
    result = result.replace("_", "")
    result = result.replace("*", "")
    result = result.replace("-", "")
    result = result.replace("+", "")
    result = result.replace("(", "")
    result = result.replace(")", "")
    result = result.replace("^", "")
    result = result.replace("%", "")
    result = result.replace("$", "")
    result = result.replace("@", "")
    result = result.replace("!", "")
    result = result.replace("&", "")
    result = result.replace(",", "")
    result = result.replace("#", "")
    result = result.replace("|", "")
    result = result.replace("\\", "")
    result = result.replace("/", "")
    result = result.replace("\"\"", "")
    result = result.replace("\"", "")
    result = predict_gender(result.replace("~", ""))
    print(result)
    return result


if __name__ == "__main__":
    processing = functions()
    stemmer = nltk.stem.PorterStemmer()
    f = open("cancerType_results.json", "w+")
    tweet_count = 0
    for x in range(3, 30):
        fread = open("outputDir/2018-03-"+str(x)+".json", "r")
        tweet_count = analyze_file(fread, tweet_count)

    for x in range(3, 24):
        fread = open("outputDir/2018-06-"+str(x)+".json", "r")
        tweet_count = analyze_file(fread, tweet_count)

    for x in range(9, 26):
        fread = open("outputDir/2018-07-"+str(x)+".json", "r")
        tweet_count = analyze_file(fread, tweet_count)

    json.dump(staged_list, f)
    f.write('\n')

    staged_gender = {
        'staged_list_stomach': staged_list_stomach,
        'staged_list_breast': staged_list_breast,
        'staged_list_blood': staged_list_blood,
        'staged_list_skin': staged_list_skin,
        'staged_list_bone': staged_list_bone,
        'staged_list_head_neck': staged_list_head_neck,
        'staged_list_lung': staged_list_lung,
        'staged_list_pediatric': staged_list_pediatric,
        'staged_list_brain': staged_list_brain}
    json.dump(staged_gender, f)
    f.write('\n')

    staged_age = {
        'staged_age_stomach': staged_age_stomach,
        'staged_age_breast': staged_age_breast,
        'staged_age_blood': staged_age_blood,
        'staged_age_skin': staged_age_skin,
        'staged_age_bone': staged_age_bone,
        'staged_age_head_neck': staged_age_head_neck,
        'staged_age_lung': staged_age_lung,
        'staged_age_pediatric': staged_age_pediatric,
        'staged_age_brain': staged_age_brain}
    json.dump(staged_age, f)
    f.write('\n')

    f.write(str(staged_gender_total))

    processing.stop_firebase()
    f.close()
