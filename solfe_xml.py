#!/bin/env python
from music21 import *
from common import cromatic
import pathlib
import sys
import argparse
from subprocess import run
import tempfile  # Added this line

parser = argparse.ArgumentParser()
parser.add_argument('infile', help='infile')
parser.add_argument('outfile', help='outfile')

args = parser.parse_args()
infilep = pathlib.Path(args.infile)

score = converter.parse(infilep)

key = score.analyze('key')
print(f"Key of the song: {key}")

num_sharps_flats = key.sharps
print(f"Number of sharps or flats: {num_sharps_flats}")

key_diff = -num_sharps_flats

cantus = score.parts[0]

new_score = stream.Score()

tempo = cantus.metronomeMarkBoundaries()[0][-1]
new_score.insert(0, tempo)


for i, measure in enumerate(cantus.getElementsByClass(stream.Measure), start=1):
    for n in measure.notesAndRests:
        if isinstance(n, note.Note):
            new_note = note.Note( pitch=60+int(key_diff), 
                                        quarterLength=n.quarterLength,
                                        lyric=cromatic[(n.pitch.midi + key_diff) % 12]
                                        )
            new_note.tie = n.tie
            new_score.append(new_note)
        elif isinstance(n, note.Rest):
            new_score.append(note.Rest(quarterLength=n.quarterLength))

    new_score[-1].tie = None

    for n in measure.notesAndRests:
        if isinstance(n, note.Note):
            n.lyric = cromatic[(n.pitch.midi + key_diff) % 12]
        new_score.append(n)

    new_score[-1].tie = None

       
new_score.write('xml', fp=args.outfile)
