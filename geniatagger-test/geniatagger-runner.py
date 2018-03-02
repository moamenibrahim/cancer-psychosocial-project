# pip install geniatagger
# or download and install from: https://pypi.python.org/pypi/geniatagger-python/0.1
# python setup.py install
import geniatagger
import os 
# Path to the original geniatagger downloaded from: http://www.nactem.ac.uk/GENIA/tagger/
# Path should go as follows: path/geniatagger
tagger = geniatagger.GeniaTagger(
    '/home/moamen/work/cancer_project/geniatagger-3.0.2/geniatagger')

f1 = open("sample.txt","r")
f = open("output.txt","w+")
output=f1.read()

# input text
print tagger.parse('Cancer Inhibition of NF-kappaB activation reversed the anti-apoptotic effect of isochamaejasmin.')
print tagger.parse('cancer Tumor Leukemia Neuroblastoma Paraganglioma Retinoblastoma Astrocytomas Retinoblastoma Lymphoma Melanoma')
out=tagger.parse(output)
f.write(str(out))

#  Chunks are represented in the IOB2 format (B for BEGIN, I for INSIDE, and O for OUTSIDE).
