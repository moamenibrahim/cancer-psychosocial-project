# pip install geniatagger
# or download and install from: https://pypi.python.org/pypi/geniatagger-python/0.1
# python setup.py install
import geniatagger

# Path to the original geniatagger downloaded from: http://www.nactem.ac.uk/GENIA/tagger/
# Path should go as follows: path/geniatagger
tagger = geniatagger.GeniaTagger(
    '/home/moamen/work/cancer_project/geniatagger-3.0.2/geniatagger')

# input text
print tagger.parse('This is a pen.')


#  Chunks are represented in the IOB2 format (B for BEGIN, I for INSIDE, and O for OUTSIDE).
