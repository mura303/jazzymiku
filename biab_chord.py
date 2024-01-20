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

bass_in = score.parts[0]
melody_in = score.parts[-1]  # 最後のパートがメロディーと仮定
print(f"bass_part: {bass_in.partName}")
print(f"melody_part: {melody_in.partName}")


key = score.analyze('key')
print(f"Key of the song: {key}")

num_sharps_flats = key.sharps
print(f"Number of sharps or flats: {num_sharps_flats}")

key_diff = num_sharps_flats


beats_per_measure = bass_in.getTimeSignatures()[0].numerator

bass_out = stream.Score()
melody_out = stream.Score()

tempo = bass_in.metronomeMarkBoundaries()[0][-1]
bass_out.insert(0, tempo)
melody_out.insert(0, tempo)
last_pitch = None # おかしな楽譜だとありえるので例外が出るようにしておく

for i, measure in enumerate(bass_in.getElementsByClass(stream.Measure)):
    if i<2:
        bass_out.append(note.Rest(quarterLength=4))
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
            bass_out.append(note.Note(pitch=pitch, quarterLength=beats[i],
                                      lyric=cromatic[(pitch+key_diff) % 12]))
            last_pitch = pitch
    else:
        bass_out.append(note.Note(pitch=last_pitch, quarterLength=4,
                                  lyric=cromatic[(last_pitch+key_diff) % 12]))


def too_long_tie(last_note):
    if isinstance(last_note, note.Rest): # 変換されて休符になってる
        return True
    if last_note.tie and last_note.tie.type == "stop":
        return True
    return False


for measure in melody_in.getElementsByClass(stream.Measure):
    for n in measure.notesAndRests:
        if isinstance(n, note.Note):
            if n.tie and too_long_tie(melody_out[-1]):  # タイの先頭以外は休符にする、NEUTRINOが変になるから
                melody_out.append(note.Rest(quarterLength=n.quarterLength))
            else:
                new_note = note.Note(pitch=n.pitch.midi,
                                     quarterLength=n.quarterLength,
                                     lyric=cromatic[(n.pitch.midi+key_diff) % 12]
                                     )
                new_note.tie = n.tie
                if new_note.tie and new_note.tie.type == "continue":
                    new_note.tie.type = "stop"
                melody_out.append(new_note)
        elif isinstance(n, note.Rest):
            melody_out.append(note.Rest(quarterLength=n.quarterLength))



bass_out.write('xml', fp=args.outfile)
melody_out.write('xml', fp=args.outfile+"melody.musicxml")
