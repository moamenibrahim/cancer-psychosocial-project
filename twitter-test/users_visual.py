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
data_sentiment=list()

named_fail=0
named_count_fail=0
pos_fail=0
topic_fail=0
sentiment_fail=0
dict_fail=0
length_fail=0

for x in range(2014,2019):

    staged_pos.append({})
    staged_hyponyms.append({})
    staged_length.append({})
    staged_named.append({})
    staged_sentiment.append({})
    staged_topic.append({})
    staged_dict.append({})
    staged_named_count.append({})

    tweet_count=0

    f = open("twitter-test/time_div/results/user_results_"+str(x)+".json", "r")
    print(f)

    # Get and populate results
    for line in f.readlines():
        
        tweet_count=tweet_count+1

        tweet_data = json.loads(line)
        # print(tweet_data)
        try:
            # Named count - Bar 
            named_count = tweet_data['Named Count']
            if (named_count != ''):
                if (named_count in staged_named_count[x-2014]):
                    ## increment that named_count
                    staged_named_count[x-2014][named_count] += 1
                else:
                    ## add named_count to list
                    staged_named_count[x-2014][named_count] = 1    
        except Exception as KeyError:
            named_count_fail+=1

        # Length - Bar 
        try:
            length = tweet_data['tweet length']
            if (length != ''):
                if (length in staged_length[x-2014]):
                    ## increment that length
                    staged_length[x-2014][length] += 1
                else:
                    ## add length to list
                    staged_length[x-2014][length] = 1
        except Exception as KeyError:
            length_fail+=1

        # Dictionary - sucess rate bar 
        try:
            dict_result = tweet_data['check_dictionary']*100
            rounded = round(dict_result)
            if (rounded in staged_dict[x-2014]):
                ## increment that rounded
                staged_dict[x-2014][rounded] += 1
            else:
                ## add rounded to list
                staged_dict[x-2014][rounded] = 1
        except Exception as KeyError:
            dict_fail+=1


        # POS - Bar
        try:
            all_elements = tweet_data['pos']
            for pos in all_elements[0]:
                if ((pos[0] != '') and (pos[0] != '.') and (pos[0] != ',') 
                and (pos[0] != '#') and (pos[0] != ':') and (pos[0] != '\'\'') 
                and (pos[0] != ')') and (pos[0] != '(') and (pos[0] != '\"\"') 
                and (pos[0] != '$') and (pos[0] != '``')):
                    if (pos[0] in staged_pos[x-2014]):
                        ## increment that pos
                        staged_pos[x-2014][pos[0]] += 1
                    else:
                        ## add pos to list
                        staged_pos[x-2014][pos[0]] = pos[1]
        except Exception as KeyError:
            pos_fail+=1


        # Topic - Bar 
        try:
            all_topic = tweet_data['topic']
            filtered_topics = [w for w in all_topic if not w in set(stopwords.words('english'))]
            filtered_topics = [w for w in filtered_topics if not w in list(string.punctuation)]
            filtered_topics = [porter.stem(word) for word in filtered_topics]

            if(len(filtered_topics)>3):
                for topic in filtered_topics:
                    if (topic != '' and len(topic)>3):
                        if (topic in staged_topic[x-2014]):
                            ## increment that topic
                            staged_topic[x-2014][topic] += 1
                        else:
                            ## add topic to list
                            staged_topic[x-2014][topic] = 1
        except Exception as KeyError:
            topic_fail+=1


        # Named-entity - Bar
        try:
            all_named = tweet_data['named entity']
            all_named = [w for w in all_named if not w in list(string.punctuation)]

            for named in all_named:
                if (named[1] != ''):
                    if (named[1] in staged_named[x-2014]):
                        ## increment that named
                        staged_named[x-2014][named[1]] += 1
                    else:
                        ## add named to list
                        staged_named[x-2014][named[1]] = 1    
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
                if (sentiment_n in staged_sentiment[x-2014]):
                    ## increment that Sentiment
                    staged_sentiment[x-2014][sentiment_n] += 1
                else:
                    ## add Sentiment to list
                    staged_sentiment[x-2014][sentiment_n] = 1
        except Exception as KeyError:
            sentiment_fail+=1

    x_axis=[]
    y_axis=[]
    for pos_key,pos_value in staged_pos[x-2014].items():
        x_axis.append(pos_key)
        y_axis.append(pos_value)
    data_pos.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))

    x_axis=[]
    y_axis=[]
    for named_key,named_value in staged_named[x-2014].items():
        x_axis.append(named_key)
        y_axis.append(named_value)
    data_named.append(go.Bar(
        x=x_axis[1:],
        y=y_axis[1:],
        name=str(x)
    ))

    x_axis=[]
    y_axis=[]
    for topic_key,topic_value in staged_topic[x-2014].items():
        x_axis.append(topic_key)
        y_axis.append(topic_value)
    data_topic.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))

    x_axis=[]
    y_axis=[]
    for dict_key,dict_value in staged_dict[x-2014].items():
        x_axis.append(dict_key)
        y_axis.append(dict_value)
    data_dict.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))

    x_axis = []
    y_axis = []
    for length_v in staged_length[x-2014].items():
        x_axis.append(length_v[0])
        y_axis.append(length_v[1])
    data_length.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))
  
    x_axis = []
    y_axis = []
    for named_count_v in staged_named_count[x-2014].items():
        x_axis.append(named_count_v[0])
        y_axis.append(named_count_v[1])
    data_named_count.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))
    
    x_axis = []
    y_axis = []
    for sentiment_v in staged_sentiment[x-2014].items():
        x_axis.append(sentiment_v[0])
        y_axis.append(sentiment_v[1])
    data_sentiment.append(go.Bar(
        x=x_axis,
        y=y_axis,
        name=str(x)
    ))

print("named_fail: %d named_count_fail: %d pos_fail: %d topic_fail: %d sentiment_fail: %d dict_fail: %d length_fail: %d "
    %(named_fail,named_count_fail,pos_fail,topic_fail,sentiment_fail,dict_fail,length_fail))


### VISUALIZATION SECTION ###
data_pos_total=[data_pos[0], data_pos[1], data_pos[2], data_pos[3], data_pos[4]]
data_named_total=[data_named[0], data_named[1], data_named[2], data_named[3], data_named[4]]
data_dict_total=[data_dict[0], data_dict[1], data_dict[2], data_dict[3], data_dict[4]]
data_topic_total=[data_topic[0], data_topic[1], data_topic[2], data_topic[3], data_topic[4]]
data_named_count_total=[data_named_count[0], data_named_count[1], data_named_count[2], data_named_count[3], data_named_count[4]]
data_length_total=[data_length[0], data_length[1], data_length[2], data_length[3], data_length[4]]
data_sentiment_total=[data_sentiment[0], data_sentiment[1], data_sentiment[2], data_sentiment[3], data_sentiment[4]]


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
# py.plot(fig, filename='dictionary-items-bar-users')

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
# py.plot(fig, filename='named-count-detected--users')

# Visualize Results
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
        title='Frequency',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data_sentiment_total, layout=layout)
py.plot(fig, filename='Sentiment-bar-users')