# Download and install from: https://pypi.python.org/pypi/geniatagger-python/0.1
# python setup.py install
import geniatagger
import os
import time

# Path to the original geniatagger downloaded from: http://www.nactem.ac.uk/GENIA/tagger/
# Path should go as follows: path/geniatagger
tagger = geniatagger.GeniaTagger(
    '/home/moamen/work/cancer_project/geniatagger-3.0.2/geniatagger')
time.sleep(7)
print "starting to process text"
# File read and write operations
fread = open("sample.txt", "r")
fwrite = open("output.txt", "w+")

#  Chunks are represented in the IOB2 format (B for BEGIN, I for INSIDE, and O for OUTSIDE).
for line in fread.readlines():
    out = tagger.parse(line)
    fwrite.writelines(str(out)+'\n')
