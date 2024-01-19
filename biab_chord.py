from music21 import *
import pathlib
import sys
import argparse
from common import cromatic

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Input file to be parsed")
parser.add_argument('outfile', help='outfile')
args = parser.parse_args()

score = converter.parse(args.file)

cantus = score.parts[0]


key = score.analyze('key')
print(f"Key of the song: {key}")

num_sharps_flats = key.sharps
print(f"Number of sharps or flats: {num_sharps_flats}")

key_diff = num_sharps_flats


beats_per_measure = cantus.getTimeSignatures()[0].numerator

new_score = stream.Score()
tempo = cantus.metronomeMarkBoundaries()[0][-1]
new_score.insert(0, tempo)


for i, measure in enumerate(cantus.getElementsByClass(stream.Measure)):
    if i<2:
        new_score.append(note.Rest( quarterLength=4 ))
        continue

    chords = list(measure.recurse().getElementsByClass('Harmony'))
    
    if len(chords)>0:
        beats = [chords[i+1].beat - chords[i].beat for i in range(len(chords)-1)]
        beats.append(beats_per_measure-sum(beats))
        
        for i, c in enumerate(chords):
            pitch = c.bass().midi
            # ピアノの右手の範囲にpitchを変換
            while pitch < 60:
                pitch += 12
            while pitch > 84:
                pitch -= 12
            new_score.append( note.Note( pitch=pitch, quarterLength=beats[i], 
                                         lyric = cromatic[(pitch+key_diff) % 12]) )
            last_pitch = pitch
    else:
        new_score.append(note.Note( pitch=last_pitch, quarterLength=4,
                                    lyric = cromatic[(pitch+key_diff) % 12]) )

    
new_score.write('xml', fp=args.outfile)
