from music21 import *
import pathlib
import sys
import argparse
from common import cromatic

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Input file to be parsed")
parser.add_argument('outfile', help='outfile')
parser.add_argument('--measurenum', help='melody')
parser.add_argument('--keydiff', help='key differece semitones. G=7, F=5, C=0, D=2')
args = parser.parse_args()

score = converter.parse(args.file)


if args.measurenum:
    measure_par_chorus = int(args.measurenum)
else:
    measure_par_chorus = 32

bass_in = score.parts[0]
print(f"bass_part: {bass_in.partName}")

key = score.analyze('key')
print(f"analyzed key of the song: {key}")

if args.keydiff:
    key_diff = -int(args.keydiff)
else:
    key_diff = -(key.tonic.midi % 12)

print(f"key diff: {key_diff}")


beats_per_measure = bass_in.getTimeSignatures()[0].numerator

bass_out = stream.Score()

tempo = bass_in.metronomeMarkBoundaries()[0][-1]
bass_out.insert(0, tempo)
last_pitch = None # おかしな楽譜だとありえるので例外が出るようにしておく


for i, measure in enumerate(bass_in.getElementsByClass(stream.Measure)):
    if i == 2+measure_par_chorus:
        break
    for n in measure.notesAndRests:
        if isinstance(n, note.Note):
            if n.tie and n.tie.type in ["continue", "stop"]:
                lyric = 'ー'
            else:
                lyric = cromatic[(n.pitch.midi + key_diff) % 12]
            new_note = note.Note(pitch=24+n.pitch.midi, 
                                 quarterLength=n.quarterLength,
                                 lyric=lyric)
            new_note.tie = n.tie
            bass_out.append(new_note)
        elif isinstance(n, note.Rest):
            bass_out.append(note.Rest(quarterLength=n.quarterLength))


bass_out.write('xml', fp=args.outfile)
