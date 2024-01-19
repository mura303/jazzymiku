from music21 import *
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Input file to be parsed")
parser.add_argument("outfile")
args = parser.parse_args()

score = converter.parse(args.infile)

cantus = score.parts[0]

for i, n in enumerate(cantus.recurse().getElementsByClass('Note')):
    print(n)

score.write('xml', fp=args.outfile)

#score.show()
