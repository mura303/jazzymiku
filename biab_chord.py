from music21 import *
import pathlib
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Input file to be parsed")
parser.add_argument('outfile', help='outfile')
args = parser.parse_args()

score = converter.parse(args.file)

cantus = score.parts[0]

beats_per_measure = cantus.getTimeSignatures()[0].numerator

new_score = stream.Score()


for i, measure in enumerate(cantus.getElementsByClass(stream.Measure)):
    if i<2:
        new_score.append(note.Rest( quarterLength=4 ))
        continue

    chords = list(measure.recurse().getElementsByClass('Harmony'))
    
    if len(chords)>0:
        beats = [chords[i+1].beat - chords[i].beat for i in range(len(chords)-1)]
        beats.append(beats_per_measure-sum(beats))
        
        for i, c in enumerate(chords):
            new_score.append( note.Note( pitch=c.bass().midi, quarterLength=beats[i]) )
            last_pitch = c.bass().midi
    else:
        new_score.append(note.Note( pitch=last_pitch, quarterLength=4 ))

    
new_score.write('xml', fp=args.outfile)
