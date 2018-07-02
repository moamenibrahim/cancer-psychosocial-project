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


""" list for family related keywords and queries """
family_list = [ "family",
                "father",
                "son",
                "daughter",
                "mother",
                "boyfriend",
                "girlfriend",
                "spouse",
                "husband",
                "wife"]

""" list for friend related keywords and queries """
friend_list =["friends",
              "friendship",
              "relation",
              "school"]
              
""" list for money related keywords and queries """
money_list =["money",
            "friends",
             "price",
             "dollars",
             "euros",
             "saving",
             "savings"
             ,"cost"]

""" list for treatment related keywords and queries """
treatment_list =["treatment",
             "radiotherapy",
             "surgical",
             "surgery",
             "pharma",
             "chemotherapy",
             "diagnosis"]



staged_hyponyms = {}
staged_topic = {}

staged_list = {}

# Get and populate results
for line in f.readlines():
    tweet_data = json.loads(line)
    repeated=0
    # print("----------------------------------------------")
    # Topic - Bar 
    try:
        all_topic = tweet_data['topic']
        hyponyms = tweet_data['hyponyms']
        
        # TODO: Check and add hyponyms 
        print(all_topic)

        if any(word in all_topic for word in family_list):
            repeated=+1
            # print('listed')
            if ('family' in staged_list):
                ## increment that topic
                staged_list['family'] += 1
            else:
                ## add topic to list
                # staged_list.add('family')
                staged_list['family'] = 1

        if any(word in all_topic for word in friend_list):
            repeated=+1
            # print('listed')
            if ('friend' in staged_list):
                ## increment that topic
                staged_list['friend'] += 1
            else:
                ## add topic to list
                staged_list['friend'] = 1

        if any(word in all_topic for word in money_list):
            repeated=+1
            # print('listed')
            if ('money' in staged_list):
                ## increment that topic
                staged_list['money'] += 1
            else:
                ## add topic to list
                staged_list['money'] = 1
            
        if any(word in all_topic for word in treatment_list):
            repeated=+1
            # print('listed')
            if ('treatment' in staged_list):
                ## increment that topic
                staged_list['treatment'] += 1
            else:
                ## add topic to list
                staged_list['treatment'] = 1   
        
        if(repeated>1):
            print(repeated)
    except:
        print("didn't translate this one - topic")


print(staged_list)

staged_list = sorted(staged_list.items(),
                      key=operator.itemgetter(1), reverse=True)

# Visualize Results     
x_axis=[]
y_axis=[]
for dict_item in staged_list:
    x_axis.append(dict_item[0])
    y_axis.append(dict_item[1])
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
py.plot(data, filename='Categorization')