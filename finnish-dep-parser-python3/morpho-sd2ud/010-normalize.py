#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Read and write CoNLL format to normalize e.g. the ordering of
# features. Also map compound word separator in lemmas.

from __future__ import print_function
from builtins import str
from past.builtins import basestring
import sys
import os
import codecs

from morphoconllu import read_conllu

usage = '%s IN OUT' % os.path.basename(__file__)

def normalize_lemma(sentence):
    for w in sentence.words():
        w.lemma = w.lemma.replace('|', '#')

def process(inf, outf):
    for s in read_conllu(inf):
        if not isinstance(s, basestring): # skip comments and sentence breaks
            normalize_lemma(s)
        print(str(s), file=outf)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) != 3:
        print('Usage:', usage, file=sys.stderr)
        return 1

    infn, outfn = argv[1], argv[2]

    with codecs.open(infn, encoding='utf-8') as inf:
        with codecs.open(outfn, 'w', encoding='utf-8') as outf:
            process(inf, outf)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
