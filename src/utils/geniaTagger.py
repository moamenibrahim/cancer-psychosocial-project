# Download and install from: https://pypi.python.org/pypi/geniatagger-python/0.1
# python setup.py install
# Path to the original geniatagger downloaded from: http://www.nactem.ac.uk/GENIA/tagger/
# Path should go as follows: path/geniatagger

import geniatagger
import os
import time

def analyze(text):
    tagger = geniatagger.GeniaTagger('/home/moamen/work/cancer_project/geniatagger-3.0.2/geniatagger')
    return tagger.parse(text)
