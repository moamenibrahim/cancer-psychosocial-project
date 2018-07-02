import os
import sys
import json
import re
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import operator
from nltk.corpus import stopwords

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
staged_named_count={}

# Get and populate results
for line in f.readlines():
    tweet_data = json.loads(line)

    try:
        # Named count - Bar 
        named_count = tweet_data['Named count']
        print(named_count)
        if (named_count != ''):
            if (named_count in staged_named_count):
                ## increment that named_count
                staged_named_count[named_count] += 1
            else:
                ## add named_count to list
                staged_named_count[named_count] = 1    
    except:
        print("didn't get this one - named count")


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
        filtered_topics = [w for w in all_topic if not w in set(stopwords.words('english'))]

        for topic in filtered_topics:
            if (topic != ''):
                if (topic in staged_topic):
                    ## increment that topic
                    staged_topic[topic] += 1
                else:
                    ## add topic to list
                    staged_topic[topic] = 1
    except:
        print("didn't get this one - topic")


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
<<<<<<< HEAD
=======

print(staged_named_count)
>>>>>>> 9f7ea3ff840a8dbc39bcc4a2b5d3c99da42ebfdd

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
        title='Number of occurence in total',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='part-of-speech-bar-2')

# Visualize Results     
x_axis=[]
y_axis=[]
for named in staged_named:
    x_axis.append(named[0])
    y_axis.append(named[1])
data = [go.Bar(
    x=x_axis[1:],
    y=y_axis[1:]
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
        title='Number of occurence in total',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='named-entity-bar-2')

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
layout = go.Layout(
    title='Extracted topics',
    xaxis=dict(
        title='Topics',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Number of occurence in total',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='topics-bar-2')

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
layout = go.Layout(
    title='Dictionary hits',
    xaxis=dict(
        title='Percentage of success',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Number of occurence in total (tweets)',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='dictionary-items-bar-2')

# Visualize Results
x_axis = []
y_axis = []
for length in staged_length:
    x_axis.append(length[0])
    y_axis.append(length[1])
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
    title='Tweets length',
    xaxis=dict(
        title='characters',    #EDIT 
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Number of occurence',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='tweets-length-bar-2')

# Visualize Results
x_axis = []
y_axis = []
for lang in staged_lang:
    x_axis.append(lang[0])
    y_axis.append(lang[1])
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
        title='Number of tweets',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='tweets-lang-bar-2')


# Visualize Results
x_axis = []
y_axis = []
for named_count in staged_named_count:
    x_axis.append(named_count[0])
    y_axis.append(named_count[1])
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
        title='Number of times detected',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='named-count-detected-bar-2')
<<<<<<< HEAD
=======

# # Sentiment - Bar 
# sentiment = tweet_data['sentiment']
# if (sentiment != ''):
#     if (sentiment in staged_sentiment):
#         ## increment that Sentiment
#         staged_sentiment[sentiment] += 1
#     else:
#         ## add Sentiment to list
#         staged_sentiment[sentiment] = 1

>>>>>>> 9f7ea3ff840a8dbc39bcc4a2b5d3c99da42ebfdd
