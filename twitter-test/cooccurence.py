import json, nltk, collections, re, string, itertools
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from keywords_helper import cancer_keywords as cancer
import json, nltk, collections, re, string, itertools
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from keywords_helper import cancer_keywords as cancer
import plotly.plotly as py
import plotly.graph_objs as go
import plotly


wordcount = {}
failed=0
stop_words = set(stopwords.words('english'))
filename="stream_results.json"
# occurenceFile="occurence.txt"
occurenceFile="twitter-test/occurence.json"
tweet_count=0
staged_word=[]
staged_word.append({})
staged_word.append({})
staged_word.append({})
staged_word.append({})
staged_word.append({})

plotly.tools.set_credentials_file(
    username='moamenibrahim', api_key='mV0gCyPj5sIKGQqC78zC')

data_word=list()

def addToArray(word,index):
    check_word=word.split(',')
    if (check_word[0] in cancer.mylist):
        pass
        print(word)
    else:
        if (word in staged_word[index]):
            ## increment that word
            staged_word[index][word] += 1
        else:
            ## add word to list
            staged_word[index][word] = 1 

def formatIntoDict(items):
    itemList={}
    for w in items:
        itemList[w]=1
    return itemList

def addDistance(dist):
    # a = {"1-2":0,"3-5":0,"6-8":0,"8-14":0,"15+":0}
    a={}
    if dist<3:
        a["1-2"]=1
    elif dist<6:
        a["3-5"]=1
    elif dist<9:
        a["6-8"]=1
    elif dist<15:
        a["8-14"]=1
    else:
        a["15+"]=1
    return a

# Helper function to remove odd characters from single words
def checkWord(wrd):
    return re.sub(r'[^\w0-9]','',wrd)

def checkSentence(string):
    ret = []
    tmp=""
    for w in string:
        w=checkWord(w)
        w=w.lower()
        if w in stop_words:
            # print(w)
            # tmp+="<poistettu>"+" "
            continue
        tmp+=w+" "
    ret.append(tmp)
    return ret

def occurenceCount(sentence):
    sents = nltk.sent_tokenize(string)
    for s in sents:
        tokens = nltk.word_tokenize(s)
        if tokens:
            pass

def findDistance(w1,w2,tweet):
    words=tweet.split()
    if w1 in words and w2 in words:
        w1_indexes = [index for index, value in enumerate(words) if value == w1]    
        w2_indexes = [index for index, value in enumerate(words) if value == w2]    
        distances = [abs(item[0] - item[1]) for item in itertools.product(w1_indexes, w2_indexes)]
        return {'min': min(distances), 'avg': sum(distances)/float(len(distances))}

def bagOfWords(texts):
    bagsofwords = [collections.Counter(re.findall(r'\w+', str(txt))) for txt in texts]
    sumbags = sum(bagsofwords, collections.Counter())
    return sumbags

def remove_stopWords(tweet):
    """ Removing english stop words from the text sent 
    including punctuations 
    """
    exclude = set(string.punctuation)
    word_tokens = nltk.word_tokenize(tweet)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    punc_free = ' '.join(ch for ch in filtered_sentence if ch not in exclude)
    return filtered_sentence

### Co-occurence process starts here
with open(filename) as f:
    sentences=[]
    tweets=[]
    # Get and populate results
    for line in f.readlines():
        tweet_data = json.loads(line)
        try:
            pure=remove_stopWords(tweet_data['translation'])
            tweets.append(pure)
            sentence=checkSentence(pure)
            sentences.append(sentence)
        except KeyError:
            failed+=1

    # print(sentences)

    ### GET REPEATED (CHECK VISUALIZE.PY) -- BAG OF WORDS
    # words=bagOfWords(sentences)
    # with open("logs.txt","w+") as myfile:
    #     myfile.write(str(words))

    ### FIND DISTANCE 
    with open(occurenceFile) as writefile:

        repeated={'people': 1865, 'good': 1711, 'democracy': 1489, 'one': 1487, 'like': 1482, 'party': 1322, 'get': 1239, 'time': 1220, 'would': 1118, 'also': 1101, 'think': 1092, 'today': 1066, 'social': 1048, 'sweden': 973, 'well': 951, 'want': 950, 'new': 937, 'see': 928, 'yes': 898, 'know': 897, 'democrats': 864, 'even': 825, 'go': 817, 'many': 777, 'right': 771, 'day': 763, 'work': 754, 'beautiful': 750, 'amp': 734, 'us': 711, 'world': 699, 'power': 694, 'years': 691, 'much': 682, 'take': 668, 'must': 645, 'care': 629, 'really': 626, 'democratic': 623, 'still': 605, 'great': 601, 'need': 582, 'make': 581, 'without': 579, 'swedish': 575, 'way': 554, 'first': 554, 'country': 545, 'left': 544, 'say': 536, 'little': 526, 'thank': 505, 'life': 498, 'cancer': 492, 'government': 478, 'year': 476, 'love': 472, 'important': 465, 'better': 465, 'something': 463, 'best': 462, 'may': 458, 'always': 454, 'two': 452, 'come': 452, 'could': 452, 'last': 446, 'read': 435, 'never': 428, 'going': 422, 'school': 414, 'medicine': 414, 'everyone': 412, 'home': 407, 'support': 405, 'back': 399, 'long': 392, 'nice': 392, 'look': 387, 'everything': 384, 'children': 381, 'give': 376, 'thanks': 376, 'understand': 373, 'free': 370, 'place': 367, 'eu': 364, 'already': 363, 'live': 363, 'said': 363, 'got': 359, 'thing': 352, 'lot': 350, 'man': 347, 'nt': 344, 'let': 344, 'bad': 343, '2': 343, 'money': 340, 'requirements': 337, 'use': 333, 'center': 333, 'course': 330, 'hope': 330, 'law': 326, 'next': 325, 'old': 324, 'person': 324, 'big': 323, 'different': 323, 'another': 317, 'summer': 315, 'state': 312, 'since': 309, 'countries': 309, 'council': 308, '1': 305, 'team': 304}
        for cancer_word in cancer:
            for repeated_word in repeated:
                for tweet in tweets:
                    if any(repeated_word in tweet):
                        distance=addDistance(findDistance(repeated_word,cancer_word,tweet))
                        towrite={repeated[repeated_word],repeated_word,cancer_word,distance,tweet}
                        json.dump(towrite, writefile, ensure_ascii=True)
                        writefile.write('\n')

    writefile.close()
f.close()

### Visualization starts here 
with open(occurenceFile) as writefile:
    for line in writefile.readlines():
        tweet_count = tweet_count + 1
        print(tweet_count)

        # tweet=line
        tweet_data = json.loads(line)
        word=tweet_data['word']
        repeated_number=tweet_data['repeated number']
        distance_loop=["1-2","3-5","6-8","8-14","15+"]
        for key in tweet_data['distance'].keys(): distance= key
        if distance==distance_loop[0]:
            addToArray(str(word)+","+str(repeated_number),0)
        elif distance==distance_loop[1]:
            addToArray(str(word)+","+str(repeated_number),1)
        elif distance==distance_loop[2]:
            addToArray(str(word)+","+str(repeated_number),2)
        elif distance==distance_loop[3]:
            addToArray(str(word)+","+str(repeated_number),3)
        elif distance==distance_loop[4]:
            addToArray(str(word)+","+str(repeated_number),4)
        else:
            print("Failed")

for x in range(0,5):
    x_axis=[]
    y_axis=[]
    for word_key,word_value in staged_word[x-1].items():
        x_axis.append(word_key)
        y_axis.append(word_value)
    data_word.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=distance_loop[x]
    ))

data_word_total=[data_word[0] , data_word[1] , data_word[2] , data_word[3] , data_word[4]]

# Visualize Results
layout = go.Layout(
    title='Co-occurence of words related to cancer',
    xaxis=dict(
        title='Proximity to cancer word',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Most frequent words, No. of times they are repeated',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data_word_total, layout=layout)
py.plot(fig, filename='Co-occurence-twitter')

print(staged_word)
writefile.close()