import os
import sys
import json
import nltk
import re
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import operator
from keywords_helper import categorization_keywords as category


stemmer = nltk.stem.PorterStemmer()

plotly.tools.set_credentials_file(
    username='moamenaibrahim', api_key='pk39TGSH9wl3WEUjWRCL')

# f = open("stream_results.json", "r")
f = open("twitter-test/stream/stream_results.json", "r")

failed=0
repeated=0
staged_sent = {}
staged_list = {'positive':{},'negative':{},'neutral':{}}

def addToArray(regularizedSentiment, mycategory):
    if (mycategory in staged_list[regularizedSentiment]):
        ## increment that topic
        staged_list[regularizedSentiment][mycategory] += 1
    else:
        ## add topic to list
        staged_list[regularizedSentiment][mycategory] = 1
    

def getSentiment(values):
    if(int(sentiment[0])<abs(int(sentiment[1]))):
        sentiment_n = int(sentiment[1])
        sentiment_m = 'negative'
    elif(int(sentiment[0])>abs(int(sentiment[1]))):
        sentiment_n = int(sentiment[0])
        sentiment_m = 'positive'
    else:
        sentiment_n=0
        sentiment_m = 'neutral'
    return sentiment_m


# Get and populate results
for line in f.readlines():

    tweet_data = json.loads(line)
    try:
        all_topic = tweet_data['topic']
        sentiment = tweet_data['sentiment']
        hyponyms = tweet_data['hyponyms']['Hyponyms']
        all_words=[x.lower() for x in all_topic+hyponyms]
        stemmed=[stemmer.stem(x.lower()) for x in all_topic+hyponyms]
        regularizedSentiment = getSentiment(sentiment)

        if (set(all_words)&set(category.family_list) or
            set(stemmed)&set(category.family_list)):
            repeated+=1
            addToArray(regularizedSentiment,'family')

        if (set(all_words)&set(category.friend_list) or
            set(stemmed)&set(category.friend_list)):
            repeated+=1
            addToArray(regularizedSentiment,'friend')

        if (set(all_words)&set(category.money_list) or
            set(stemmed)&set(category.money_list)):
            repeated+=1
            addToArray(regularizedSentiment,'money')
            
        if (set(all_words)&set(category.treatment_list) or
            set(stemmed)&set(category.treatment_list)):
            repeated+=1
            addToArray(regularizedSentiment,'treatment')
           
        if (set(all_words)&set(category.lifestyle_list) or
            set(stemmed)&set(category.lifestyle_list)):
            repeated+=1
            addToArray(regularizedSentiment,'lifestyle')
            
    except Exception as KeyError:
        failed+=1

print(staged_list)
print("failed to categorize %d"%failed)
print("overall repetition %d"%repeated)

traces=[]
# Visualize Results     
for target in staged_list:
    x_axis=[]
    y_axis=[]
    for key,value in staged_list[target].items():
        x_axis.append(key)
        y_axis.append(value/repeated*100)
    data = go.Bar(
        x=x_axis,
        y=y_axis,
        name=target
    )
    traces.append(data)

layout = go.Layout(
    barmode='stack',
    title='Categorization',
    xaxis=dict(
        title='Categories',
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
fig = go.Figure(data=traces, layout=layout)
py.plot(fig, filename='Categorization-with-sentiment')