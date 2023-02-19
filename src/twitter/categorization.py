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

f = open("twitter-test/stream/stream_results.json", "r")

staged_list = {}
failed = 0
repeated = 0

# Get and populate results
for line in f.readlines():

    tweet_data = json.loads(line)
    try:
        all_topic = tweet_data['topic']
        hyponyms = tweet_data['hyponyms']['Hyponyms']

        if (any(word in all_topic for word in category.family_list)
            or any(stemmer.stem(word) in all_topic for word in category.family_list)
                or any(word in hyponyms for word in category.family_list)):
            repeated += 1
            if ('family' in staged_list):
                # increment that topic
                staged_list['family'] += 1
            else:
                # add topic to list
                staged_list['family'] = 1

        if (any(word in all_topic for word in category.friend_list)
            or any(stemmer.stem(word) in all_topic for word in category.friend_list)
                or any(word in hyponyms for word in category.friend_list)):
            repeated += 1
            if ('friend' in staged_list):
                # increment that topic
                staged_list['friend'] += 1
            else:
                # add topic to list
                staged_list['friend'] = 1

        if (any(word in all_topic for word in category.money_list)
            or any(stemmer.stem(word) in all_topic for word in category.money_list)
                or any(word in hyponyms for word in category.money_list)):
            repeated += 1
            if ('money' in staged_list):
                # increment that topic
                staged_list['money'] += 1
            else:
                # add topic to list
                staged_list['money'] = 1

        if (any(word in all_topic for word in category.treatment_list)
            or any(stemmer.stem(word) in all_topic for word in category.treatment_list)
                or any(word in hyponyms for word in category.treatment_list)):
            repeated += 1
            if ('treatment' in staged_list):
                # increment that topic
                staged_list['treatment'] += 1
            else:
                # add topic to list
                staged_list['treatment'] = 1

        if (any(word in all_topic for word in category.lifestyle_list)
            or any(stemmer.stem(word) in all_topic for word in category.lifestyle_list)
                or any(word in hyponyms for word in category.lifestyle_list)):
            repeated += 1
            if ('lifestyle' in staged_list):
                # increment that topic
                staged_list['lifestyle'] += 1
            else:
                # add topic to list
                staged_list['lifestyle'] = 1

    except Exception as KeyError:
        failed += 1

print(staged_list)
print("failed to categorize %d" % failed)
print("overall repetition %d" % repeated)

staged_list = sorted(staged_list.items(),
                     key=operator.itemgetter(1), reverse=True)

# Visualize Results
x_axis = []
y_axis = []
for dict_item in staged_list:
    x_axis.append(dict_item[0])
    y_axis.append(dict_item[1]/repeated*100)
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
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
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='Categorization')
