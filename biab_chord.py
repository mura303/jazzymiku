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
melody_in = score.parts[-1]  # 最後のパートがメロディーと仮定
print(f"bass_part: {bass_in.partName}")
print(f"melody_part: {melody_in.partName}")


key = score.analyze('key')
print(f"Key of the song: {key}")

num_sharps_flats = key.sharps
print(f"Number of sharps or flats: {num_sharps_flats}")


if args.keydiff:
    key_diff = -int(args.keydiff)
else:
    key_diff = num_sharps_flats


beats_per_measure = bass_in.getTimeSignatures()[0].numerator

bass_out = stream.Score()
melody_out = stream.Score()

tempo = bass_in.metronomeMarkBoundaries()[0][-1]
bass_out.insert(0, tempo)
melody_out.insert(0, tempo)
last_pitch = None # おかしな楽譜だとありえるので例外が出るようにしておく

for i, measure in enumerate(bass_in.getElementsByClass(stream.Measure)):
    if i < 2:
        bass_out.append(note.Rest(quarterLength=4))
        continue
    if i == 2+measure_par_chorus:
        break

    chords = list(measure.recurse().getElementsByClass('Harmony'))
    
    if len(chords) > 0:
        beats = [chords[i+1].beat - chords[i].beat for i in range(len(chords)-1)]
        beats.append(beats_per_measure-sum(beats))
        
        for i, c in enumerate(chords):
            pitch = c.bass().midi
            # ピアノの右手の範囲にpitchを変換
            while pitch < 60:
                pitch += 12
            while pitch > 84:
                pitch -= 12
            bass_out.append(note.Note(pitch=pitch, quarterLength=beats[i],
                                      lyric=cromatic[(pitch+key_diff) % 12]))
            last_pitch = pitch
    else:
        bass_out.append(note.Note(pitch=last_pitch, quarterLength=4,
                                  lyric=cromatic[(last_pitch+key_diff) % 12]))


for i, measure in enumerate(melody_in.getElementsByClass(stream.Measure)):
    if i < 2:
        continue
    if i == 2+measure_par_chorus:
        break
    for n in measure.notesAndRests:
        if isinstance(n, note.Note):
            if n.tie and n.tie.type in ["continue", "stop"]:
                lyric = 'ー'
            else:
                lyric = cromatic[(n.pitch.midi + key_diff) % 12]
            new_note = note.Note(pitch=n.pitch.midi,
                                 quarterLength=n.quarterLength,
                                 lyric=lyric)
            new_note.tie = n.tie
            bass_out.append(new_note)
        elif isinstance(n, note.Rest):
            bass_out.append(note.Rest(quarterLength=n.quarterLength))


bass_out.write('xml', fp=args.outfile)
