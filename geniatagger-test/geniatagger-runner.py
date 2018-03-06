# Download and install from: https://pypi.python.org/pypi/geniatagger-python/0.1 
# python setup.py install 
import geniatagger
import os 
# Path to the original geniatagger downloaded from: http://www.nactem.ac.uk/GENIA/tagger/
# Path should go as follows: path/geniatagger
tagger = geniatagger.GeniaTagger('/home/moamen/work/cancer_project/geniatagger-3.0.2/geniatagger')

fread = open("sample.txt","r")
fwrite = open("output.txt","w+")

for line in fread.readlines():
    # line_text=fread.readline()
    out = tagger.parse(line)
    fwrite.writelines(str(out)+'\n')


# input text
# print tagger.parse('Cancer Inhibition of NF-kappaB activation reversed the anti-apoptotic effect of isochamaejasmin.')
# print tagger.parse('cancer Tumor Leukemia Neuroblastoma Paraganglioma Retinoblastoma Astrocytomas Retinoblastoma Lymphoma Melanoma')

#  Chunks are represented in the IOB2 format (B for BEGIN, I for INSIDE, and O for OUTSIDE).