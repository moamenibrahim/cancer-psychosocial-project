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
    username='moamenaibrahim', api_key='pk39TGSH9wl3WEUjWRCL')

f = open("twitter-test/stream/cancerType_results.json", "r")
# Get and populate results
for line in f.readlines():
    staged_pos = json.loads(line)
    break

staged_pos = sorted(staged_pos.items(),
                    key=operator.itemgetter(1), reverse=True)

# Visualize Results
x_axis = []
y_axis = []
for named_count in staged_pos:
    x_axis.append(named_count[0])
    y_axis.append(named_count[1])
data = [go.Bar(
    x=x_axis,
    y=y_axis
)]
layout = go.Layout(
    title='Cancer types detected from Streaming tweets',
    xaxis=dict(
        title='cancer_types',
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
py.plot(fig, filename='cancer_types')
