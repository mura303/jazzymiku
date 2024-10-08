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

def get_key_diff(filename):
    import xml.etree.ElementTree as ET

    tree = ET.parse(filename)
    root = tree.getroot()
    # part/measure/attributes/key/fifthsを取得
    for part in root.findall('.//part'):
        for measure in part.findall('measure'):
            for attributes in measure.findall('attributes'):
                for key in attributes.findall('key'):
                    fifths = key.find('fifths').text
                    print(f"Part ID: {part.attrib['id']}, Measure Number: {measure.attrib['number']}, Key Fifths: {fifths}")
                    key_diff = (12 + int(fifths)) * 5 % 12

    return key_diff


def get_measure_per_chorus( score_part ):
    part_measures_count = len(score_part.getElementsByClass(stream.Measure))
    print(f"パート内の小節数: {part_measures_count}")
    measure_per_chorus = int(part_measures_count - 4)
    print(f"measurenum : {measure_per_chorus}")
    return measure_per_chorus


if args.measurenum:
    measure_par_chorus = int(args.measurenum)
else:
    measure_par_chorus = get_measure_per_chorus(score.parts[0])

bass_in = score.parts[0]
melody_in = score.parts[0]  # 最後のパートがメロディーと仮定、左手右手あるから-2
print(f"bass_part: {bass_in.partName}")
print(f"melody_part: {melody_in.partName}")

#key = score.analyze('key')
#print(f"analyzed key of the song: {key}")

if args.keydiff:
    key_diff = -int(args.keydiff)
else:
    key_diff = 0 # get_key_diff(args.file)
    
print(f"key diff: {key_diff}")


beats_per_measure = bass_in.getTimeSignatures()[0].numerator

print(f"beats : {beats_per_measure}")

bass_out = stream.Score()
melody_out = stream.Score()

tempo = bass_in.metronomeMarkBoundaries()[0][-1]
bass_out.insert(0, tempo)
melody_out.insert(0, tempo)

if beats_per_measure == 3:
    bass_out.append(meter.TimeSignature('3/4'))
    melody_out.append(meter.TimeSignature('3/4'))

last_pitch = None # おかしな楽譜だとありえるので例外が出るようにしておく

for i, measure in enumerate(bass_in.expandRepeats().getElementsByClass(stream.Measure)):
    if i < 2:
        bass_out.append(note.Rest(quarterLength=beats_per_measure))
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
        bass_out.append(note.Note(pitch=last_pitch, quarterLength=beats_per_measure,
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
