from __future__ import print_function
from builtins import str
import sys
import json
import os.path
try:
    import argparse
except ImportError:
    import compat.argparse as argparse


parser = argparse.ArgumentParser(description='Options')
parser.add_argument('-d', help='Where to read the comments?')
args = parser.parse_args()

hashes=None
if args.d and os.path.isfile(args.d):
    with open(args.d,"r") as f:
        hashes=json.load(f)

comment=False
for lineIdx,line in enumerate(sys.stdin):
    line=str(line).rstrip()
    if not line or line.startswith("###START") or line.startswith("###END"):
        continue
    tokens=line.split()
    if lineIdx!=0 and comment==False: # do not print empty line after comment
        print()
#    if hashes and len(tokens)==1 and tokens[0] in hashes: # this is hashed comment, extract it
    if hashes and "".join(tokens) in hashes: # this is hashed comment, extract it, do not trust tokenizer to not split hash
        print(hashes["".join(tokens)])
        comment=True
        continue
    for tIdx,t in enumerate(tokens):
        print(("%d\t%s\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_"%(tIdx+1,t)))
        comment=False
