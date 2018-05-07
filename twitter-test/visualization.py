import os
import sys
import json
import re
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import operator

plotly.tools.set_credentials_file(
    username='moamenibrahim', api_key='mV0gCyPj5sIKGQqC78zC')

f = open("stream_results.json", "r")

staged_pos = {}
staged_lang = {}
staged_hyponyms = {}
staged_length = {}
staged_named = {}
staged_sentiment = {}
staged_topic = {}
staged_dict = {}

# Get and populate results
for line in f.readlines():
    tweet_data = json.loads(line)


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
        print(dict_result)
        rounded = round(dict_result)
        if (rounded in staged_dict):
            ## increment that rounded
            staged_dict[rounded] += 1
        else:
            ## add rounded to list
            staged_dict[rounded] = 1
    except:
        print("didn't translate this one - dictionary")


    # POS - Bar
    try:
        all_elements = tweet_data['pos']
        for pos in all_elements:
            if (pos[0] != ''):
                if (pos[0] in staged_pos):
                    ## increment that pos
                    staged_pos[pos[0]] += 1
                else:
                    ## add pos to list
                    staged_pos[pos[0]] = pos[1]
    except:
        print("didn't translate this one - pos")


    # Topic - Bar 
    try:
        all_topic = tweet_data['topic']
        for topic in all_topic:
            if (topic != ''):
                if (topic in staged_topic):
                    ## increment that topic
                    staged_topic[topic] += 1
                else:
                    ## add topic to list
                    staged_topic[topic] = 1
    except:
        print("didn't translate this one - topic")


    # Named-entity - Scatter
    try:
        all_named = tweet_data['named entity']
        for named in all_named:
            if (named[1] != ''):
                if (named[1] in staged_named):
                    ## increment that named
                    staged_named[named[1]] += 1
                else:
                    ## add named to list
                    staged_named[named[1]] = 1    
    except:
        print("didn't translate this one - named entity")


    # # Hyponyms - Scatter 
    # hyponyms = tweet_data['hyponyms']
    # if (hyponyms != ''):
    #     if (hyponyms in staged_hyponyms):
    #         ## increment that hyponyms
    #         staged_hyponyms[hyponyms] += 1
    #     else:
    #         ## add hyponyms to list
    #         staged_hyponyms[hyponyms] = 1


    # # Sentiment - Bar 
    # sentiment = tweet_data['sentiment']
    # if (sentiment != ''):
    #     if (sentiment in staged_sentiment):
    #         ## increment that Sentiment
    #         staged_sentiment[sentiment] += 1
    #     else:
    #         ## add Sentiment to list
    #         staged_sentiment[sentiment] = 1




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

# print(staged_pos)
# print(staged_length)
# print(staged_named)
# print(staged_topic)
# print(staged_dict)


# Visualize Results     
x_axis=[]
y_axis=[]
for pos in staged_pos:
    x_axis.append(pos[0])
    y_axis.append(pos[1])
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
py.plot(data, filename='part-of-speech-bar')

# Visualize Results     
x_axis=[]
y_axis=[]
for named in staged_named:
    x_axis.append(named[0])
    y_axis.append(named[1])
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
py.plot(data, filename='named-entity-bar')

# Visualize Results     
x_axis=[]
y_axis=[]
for topic in staged_topic:
    x_axis.append(topic[0])
    y_axis.append(topic[1])
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
py.plot(data, filename='topics-bar')

# Visualize Results     
x_axis=[]
y_axis=[]
for dict_item in staged_dict:
    x_axis.append(dict_item[0])
    y_axis.append(dict_item[1])
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
py.plot(data, filename='dictionary-items-bar')