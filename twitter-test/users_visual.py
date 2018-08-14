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

staged_pos = []
staged_hyponyms = []
staged_length = []
staged_named = []
staged_sentiment = []
staged_topic = []
staged_dict = []
staged_named_count = []

data_pos=list()
data_named=list()
data_length=list()
data_named_count=list()
data_dict=list()
data_topic=list()

for x in range(1,7):

    staged_pos.append({})
    staged_hyponyms.append({})
    staged_length.append({})
    staged_named.append({})
    staged_sentiment.append({})
    staged_topic.append({})
    staged_dict.append({})
    staged_named_count.append({})

    # TODO 
    f = open("users/results/user_results_"+str(x)+".json", "r")

    # Get and populate results
    for line in f.readlines():
        tweet_data = json.loads(line)

        try:
            # Named count - Bar 
            named_count = tweet_data['Named Count']
            if (named_count != ''):
                if (named_count in staged_named_count[x-1]):
                    ## increment that named_count
                    staged_named_count[x-1][named_count] += 1
                else:
                    ## add named_count to list
                    staged_named_count[x-1][named_count] = 1    
        except:
            print("didn't translate this one - named count")

        # Length - Bar 
        try:
            length = tweet_data['tweet length']
            if (length != ''):
                if (length in staged_length[x-1]):
                    ## increment that length
                    staged_length[x-1][length] += 1
                else:
                    ## add length to list
                    staged_length[x-1][length] = 1
        except:
            print("didn't translate this one - tweet length")

        # Dictionary - sucess rate bar 
        try:
            dict_result = tweet_data['check_dictionary']*100
            rounded = round(dict_result)
            if (rounded in staged_dict[x-1]):
                ## increment that rounded
                staged_dict[x-1][rounded] += 1
            else:
                ## add rounded to list
                staged_dict[x-1][rounded] = 1
        except:
            print("didn't translate this one - dictionary")


        # POS - Bar
        try:
            all_elements = tweet_data['pos']
            for pos in all_elements[0]:
                if (pos[0] != ''):
                    if (pos[0] in staged_pos[x-1]):
                        ## increment that pos
                        staged_pos[x-1][pos[0]] += 1
                    else:
                        ## add pos to list
                        staged_pos[x-1][pos[0]] = pos[1]
        except:
            print("didn't translate this one - pos")


        # Topic - Bar 
        try:
            all_topic = tweet_data['topic']
            filtered_topics = [w for w in all_topic if not w in set(stopwords.words('english'))]
            if(len(filtered_topics)>3):
                for topic in filtered_topics:
                    if (topic != '' and len(topic)>3):
                        if (topic in staged_topic[x-1]):
                            ## increment that topic
                            staged_topic[x-1][topic] += 1
                        else:
                            ## add topic to list
                            staged_topic[x-1][topic] = 1
        except:
            print("didn't translate this one - topic")


        # Named-entity - Bar
        try:
            all_named = tweet_data['named entity']
            for named in all_named:
                if (named[1] != ''):
                    if (named[1] in staged_named[x-1]):
                        ## increment that named
                        staged_named[x-1][named[1]] += 1
                    else:
                        ## add named to list
                        staged_named[x-1][named[1]] = 1    
        except:
            print("didn't translate this one - named entity")


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
                if (sentiment_n in staged_sentiment[x-1]):
                    ## increment that Sentiment
                    staged_sentiment[x-1][sentiment_n] += 1
                else:
                    ## add Sentiment to list
                    staged_sentiment[x-1][sentiment_n] = 1
        except:
            print("didn't translate this one - sentiment")

    x_axis=[]
    y_axis=[]
    for pos_key,pos_value in staged_pos[x-1].items():
        x_axis.append(pos_key)
        y_axis.append(pos_value)
    data_pos.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))

    x_axis=[]
    y_axis=[]
    for named_key,named_value in staged_named[x-1].items():
        x_axis.append(named_key)
        y_axis.append(named_value)
    data_named.append(go.Bar(
        x=x_axis[1:],
        y=y_axis[1:],
        name=str(x)
    ))

    x_axis=[]
    y_axis=[]
    for topic_key,topic_value in staged_topic[x-1].items():
        x_axis.append(topic_key)
        y_axis.append(topic_value)
    data_topic.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))

    x_axis=[]
    y_axis=[]
    for dict_key,dict_value in staged_dict[x-1].items():
        x_axis.append(dict_key)
        y_axis.append(dict_value)
    data_dict.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))

    x_axis = []
    y_axis = []
    for length_v in staged_length[x-1].items():
        x_axis.append(length_v[0])
        y_axis.append(length_v[1])
    data_length.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))
  
    x_axis = []
    y_axis = []
    for named_count_v in staged_named_count[x-1].items():
        x_axis.append(named_count_v[0])
        y_axis.append(named_count_v[1])
    data_named_count.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))


### VISUALIZATION SECTION ###
data_pos_total=[data_pos[0], data_pos[1], data_pos[2], data_pos[3], data_pos[4], data_pos[5]]
data_named_total=[data_named[0], data_named[1], data_named[2], data_named[3], data_named[4], data_named[5]]
data_dict_total=[data_dict[0], data_dict[1], data_dict[2], data_dict[3], data_dict[4], data_dict[5]]
data_topic_total=[data_topic[0], data_topic[1], data_topic[2], data_topic[3], data_topic[4], data_topic[5]]
data_named_count_total=[data_named_count[0], data_named_count[1], data_named_count[2], data_named_count[3], data_named_count[4], data_named_count[5]]
data_length_total=[data_length[0], data_length[1], data_length[2], data_length[3], data_length[4], data_length[5]]

# Visualize Results     
layout = go.Layout(
    barmode='group',
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
fig = go.Figure(data=data_pos_total, layout=layout)
py.plot(fig, filename='part-of-speech-bar-users')

# Visualize Results     
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
fig = go.Figure(data=data_named_total, layout=layout)
py.plot(fig, filename='named-entity-bar-users')

# Visualize Results     
layout = go.Layout(
    title='Extracted topics',
    xaxis=dict(
        title='Topics',
        range=[0, 50],
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
fig = go.Figure(data=data_topic_total, layout=layout)
py.plot(fig, filename='topics-bar-users')

# Visualize Results     
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
fig = go.Figure(data=data_dict_total, layout=layout)
py.plot(fig, filename='dictionary-items-bar-users')

# Visualize Results
layout = go.Layout(
    title='Tweets length',
    xaxis=dict(
        title='characters',  
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
fig = go.Figure(data=data_length_total, layout=layout)
py.plot(fig, filename='tweets-length-bar-users')

# Visualize Results
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
fig = go.Figure(data=data_named_count_total, layout=layout)
py.plot(fig, filename='named-count-detected--users')
