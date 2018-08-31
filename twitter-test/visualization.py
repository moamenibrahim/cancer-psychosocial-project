import os
import sys
import json
import re
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import operator
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


porter = PorterStemmer()

plotly.tools.set_credentials_file(
    username='moamenibrahim', api_key='mV0gCyPj5sIKGQqC78zC')

f = open("twitter-test/stream_results.json", "r")

tweets=17200

staged_pos = {}
staged_lang = {}
staged_hyponyms = {}
staged_length = {}
staged_named = {}
staged_sentiment = {}
staged_topic = {}
staged_dict = {}
staged_named_count={}

named_fail=0
named_count_fail=0
pos_fail=0
topic_fail=0
sentiment_fail=0
dict_fail=0

ORGANIZATION_count=0
PERSON_count=0
LOCATION_count=0
TIME_count=0
MONEY_count=0
DATE_count=0
PERCENT_count=0

# Get and populate results
for line in f.readlines():
    tweet_data = json.loads(line)

    try:
        # Named count - Bar 
        named_count = tweet_data['Named count']
        if (named_count != ''):
            if (named_count in staged_named_count):
                ## increment that named_count
                staged_named_count[named_count] += 1
            else:
                ## add named_count to list
                staged_named_count[named_count] = 1    
    except Exception as KeyError:
        named_count_fail+=1


    # Length - Bar 
    length = tweet_data['tweet length']
    if (length != ''):
        if (length in staged_length):
            ## increment that length
            staged_length[length] += 1
        else:
            ## add length to list
            staged_length[length] = 1


    # Language - Bar 
    lang = tweet_data['lang']
    if (lang != ''):
        if (lang in staged_lang):
            ## increment that lang
            staged_lang[lang] += 1
        else:
            ## add lang to list
            staged_lang[lang] = 1


    # Dictionary - sucess rate bar 
    try:
        dict_result = tweet_data['check_dictionary']*100
        rounded = round(dict_result)
        if (rounded in staged_dict):
            ## increment that rounded
            staged_dict[rounded] += 1
        else:
            ## add rounded to list
            staged_dict[rounded] = 1
    except Exception as KeyError:
        dict_fail+=1


    # POS - Bar
    try:
        all_elements = tweet_data['pos']
        for sentence in all_elements:
            for pos in sentence:
                if ((pos[0] != '') and (pos[0] != '.') and (pos[0] != ',') 
                and (pos[0] != '#') and (pos[0] != ':') and (pos[0] != '\'\'') 
                and (pos[0] != ')') and (pos[0] != '(') and (pos[0] != '\"\"') 
                and (pos[0] != '$') and (pos[0] != '``')):
                    if (pos[0] in staged_pos):
                        ## increment that pos
                        staged_pos[pos[0]] += 1
                    else:
                        ## add pos to list
                        staged_pos[pos[0]] = pos[1]
    except Exception as KeyError:
        pos_fail+=1


    # Topic - Bar 
    try:
        all_topic = tweet_data['topic']
        filtered_topics = [w for w in all_topic if not w in set(stopwords.words('english'))]
        filtered_topics = [w for w in filtered_topics if not w in list(string.punctuation)]
        filtered_topics = [porter.stem(word) for word in filtered_topics]

        for topic in filtered_topics:
            if (topic != ''):
                if (topic in staged_topic):
                    ## increment that topic
                    staged_topic[topic] += 1
                else:
                    ## add topic to list
                    staged_topic[topic] = 1
    except Exception as KeyError:
        topic_fail+=1


    # Named-entity - Bar
    try:
        all_named = tweet_data['named entity']
        all_named = [w for w in all_named if not w in list(string.punctuation)]

        if(bool(re.search('TIME',str(all_named)))):
            TIME_count+=1
        if(bool(re.search('ORGANIZATION',str(all_named)))):
            ORGANIZATION_count+=1
        if(bool(re.search('PERSON',str(all_named)))):
            PERSON_count+=1
        if(bool(re.search('LOCATION',str(all_named)))):
            LOCATION_count+=1
        if(bool(re.search('MONEY',str(all_named)))):
            MONEY_count+=1
        if(bool(re.search('DATE',str(all_named)))):
            DATE_count+=1
        if(bool(re.search('PERCENT',str(all_named)))):
            PERCENT_count+=1

        for named in all_named:
            if (named[1] != ''):
                if (named[1] in staged_named):
                    ## increment that named
                    staged_named[named[1]] += 1
                else:
                    ## add named to list
                    staged_named[named[1]] = 1    
    except Exception as KeyError:
        named_fail+=1



    # # Sentiment - Bar 
    try:
        sentiment = tweet_data['sentiment']
        if(int(sentiment[0])<abs(int(sentiment[1]))):
            sentiment_n = int(sentiment[1])
        elif(int(sentiment[0])>abs(int(sentiment[1]))):
            sentiment_n = int(sentiment[0])
        else:
            sentiment_n=0
        if (sentiment_n != ''):
            if (sentiment_n in staged_sentiment):
                ## increment that Sentiment
                staged_sentiment[sentiment_n] += 1
            else:
                ## add Sentiment to list
                staged_sentiment[sentiment_n] = 1
    except Exception as KeyError:
        sentiment_fail+=1


print("named_fail: %d named_count_fail: %d pos_fail: %d topic_fail: %d sentiment_fail: %d dict_fail %d"
    %(named_fail,named_count_fail,pos_fail,topic_fail,sentiment_fail,dict_fail))

staged_pos = sorted(staged_pos.items(),
                        key=operator.itemgetter(1), reverse=True)
staged_length = sorted(staged_length.items(),
                     key=operator.itemgetter(1), reverse=True)
staged_named = sorted(staged_named.items(),
                     key=operator.itemgetter(1), reverse=True)
staged_topic = sorted(staged_topic.items(),
                     key=operator.itemgetter(1), reverse=True)
staged_dict = sorted(staged_dict.items(),
                      key=operator.itemgetter(1), reverse=True)
staged_lang = sorted(staged_lang.items(),
                      key=operator.itemgetter(1), reverse=True)
staged_named_count = sorted(staged_named_count.items(),
                      key=operator.itemgetter(1), reverse=True)
staged_sentiment = sorted(staged_sentiment.items(),
                      key=operator.itemgetter(1), reverse=True)


# Visualize Results  
total = 0    
x_axis=[]
y_axis=[]
for pos_sum in staged_pos:
    total+=pos_sum[1]
print(total)
for pos in staged_pos:
    x_axis.append(pos[0])
    y_axis.append(pos[1]/total*100)
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
    title='Part-of-speech-tagging',
    xaxis=dict(
        title='POS',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentage of occurence',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='part-of-speech-bar-streaming')


# Visualize Results 
total=0
x_axis=[]
y_axis=[]
del staged_named[0]
for named_sum in staged_named:
    total+=float(named_sum[1])
print(total)
for named in staged_named:
    x_axis.append(named[0])
    y_axis.append(named[1]/total*100)
data = [go.Bar(
    x=x_axis[0:],
    y=y_axis[0:]
)]
layout = go.Layout(
    title='Named entity',
    xaxis=dict(
        title='Entities',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentage of occurence',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='named-entity-bar-streaming')


# Visualize Results 
data = [go.Bar(
    x=['ORGANIZATION','LOCATION','PERSON','TIME','DATE','MONEY','PERCENT'],
    y=[ORGANIZATION_count/tweets*100,LOCATION_count/tweets*100,PERSON_count/tweets*100,TIME_count/tweets*100,DATE_count/tweets*100,MONEY_count/tweets*100,PERCENT_count/tweets*100]
)]
layout = go.Layout(
    title='Named entity',
    xaxis=dict(
        title='Entities',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentage of Tweets',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='named-entity-percent-bar-streaming')


# Visualize Results     
x_axis=[]
y_axis=[]
for topic in staged_topic:
    x_axis.append(topic[0])
    y_axis.append(topic[1]/tweets*100)
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
    title='Extracted topics',
    xaxis=dict(
        range=[0,50],
        title='Topics',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentage of occurence',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='topics-bar-streaming')


# Visualize Results     
x_axis=[]
y_axis=[]
for dict_item in staged_dict:
    x_axis.append(dict_item[0])
    y_axis.append(dict_item[1]/tweets*100)
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
    title='Dictionary hits',
    xaxis=dict(
        title='Percentage of successful hits',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentage of tweets',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='dictionary-items-bar-streaming')


# Visualize Results
x_axis = []
y_axis = []
for length in staged_length:
    x_axis.append(length[0])
    y_axis.append(length[1]/tweets*100)
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
    title='Tweets length',
    xaxis=dict(
        title='Tweet length (words)', 
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentages of tweets',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='tweets-length-bar-streaming')


# Visualize Results
x_axis = []
y_axis = []
for lang in staged_lang:
    x_axis.append(lang[0])
    y_axis.append(lang[1]/tweets*100)
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
    title='Language dispersion',
    xaxis=dict(
        title='Languages',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentage of tweets',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='tweets-lang-bar-streaming')


# Visualize Results
x_axis = []
y_axis = []
for named_count in staged_named_count:
    x_axis.append(named_count[0])
    y_axis.append(named_count[1]/tweets*100)
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
    title='Named entity detected frequency',
    xaxis=dict(
        title='Number of named entities detected',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentage of tweets',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='named-count-detected-bar-streaming')


# Visualize Results
x_axis = []
y_axis = []
for sentiment in staged_sentiment:
    x_axis.append(sentiment[0])
    y_axis.append(sentiment[1]/tweets*100)
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
    title='Overall Sentiment Analysis',
    xaxis=dict(
        title='Sentiment score',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Percentage of tweets',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='Sentiment-bar-streaming')