#!/bin/bash
set -o pipefail
source init.sh
cat | $PYTHON check_encoding.py | opennlp SentenceDetector model/fi-sent.bin | opennlp TokenizerME model/fi-token.bin | $PYTHON txt_to_09.py
