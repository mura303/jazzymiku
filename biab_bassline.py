# band in a box でmusicxml出力して使う
# 2コーラス限定、小節数計算のため
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

key_diff = get_key_diff(args.file)

#if args.measurenum:
#    measure_par_chorus = int(args.measurenum)
#else:
#    measure_par_chorus = 32

bass_in = score.parts[0]
melody_in = score.parts[-2]  # 最後のパートがメロディーと仮定、左手右手あるから-2
print(f"bass_part: {bass_in.partName}")
print(f"melody_part: {melody_in.partName}")


def get_measure_per_chorus( score_part ):
    part_measures_count = len(score_part.getElementsByClass(stream.Measure))
    print(f"パート内の小節数: {part_measures_count}")
    measure_per_chorus = int((part_measures_count - 4)/2)
    print(f"measurenum : {measure_per_chorus}")
    return measure_per_chorus

measure_par_chorus = get_measure_per_chorus( bass_in )

#key = score.analyze('key')
#print(f"analyzed key of the song: {key}")

#if args.keydiff:
#    key_diff = -int(args.keydiff)
#else:
#    key_diff = -(key.tonic.midi % 12)

print(f"key diff: {key_diff}")

beats_per_measure = bass_in.getTimeSignatures()[0].numerator

bass_out = stream.Score()
melody_out = stream.Score()

tempo = bass_in.metronomeMarkBoundaries()[0][-1]
bass_out.insert(0, tempo)
melody_out.insert(0, tempo)
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
