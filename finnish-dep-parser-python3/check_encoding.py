from __future__ import print_function
import sys
import codecs
import os

if __name__==u"__main__":
    try:
        #utf-8-sig interprets BOM as BOM not as space
        #inp=codecs.getreader("utf-8")(os.fdopen(0,"U")) #Switches universal newlines on, so all newlines are now simply "\n"
        #inp = sys.stdin
        for line in sys.stdin:
            line=line.rstrip("\n")
            print(line) #
    except UnicodeDecodeError:
        print("Error: Input file encoding is not utf-8, terminate parsing.", file=sys.stderr)
        sys.exit(1)
