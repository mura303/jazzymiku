from music21 import *
from common import cromatic
import pathlib
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--key', '-k', help='key')
parser.add_argument('--input', '-i', help='input file')
parser.add_argument('--output', '-o', help='output file')
args = parser.parse_args()

score = converter.parse(args.input)

cantus = score.parts[0]

for i, measure in enumerate(cantus.getElementsByClass(stream.Measure), start=1):
    new_score = stream.Score()
    for n in measure.notesAndRests:
        if isinstance(n, note.Note):
            new_note = note.Note( pitch=60+int(args.key), 
                                        quarterLength=n.quarterLength,
                                        lyric=n.lyric,
                                        )
            new_note.tie = n.tie
            new_score.append(new_note)
        elif isinstance(n, note.Rest):
            new_score.append(note.Rest(quarterLength=n.quarterLength))

    new_score[-1].tie = None

    for n in measure.notesAndRests:
        new_score.append(n)

    new_score[-1].tie = None

    if len(new_score.getElementsByClass(note.Note)) > 0:
        new_score.write('xml', fp=f"{args.output}{i}.musicxml")
