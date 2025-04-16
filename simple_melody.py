from music21 import *
import pathlib
import sys
import argparse
from common import cromatic

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Input file to be parsed")
parser.add_argument('outfile', help='outfile')
parser.add_argument('-p', '--part', type=int, help='Part number to process', default=0)
parser.add_argument('-t', '--transpose', type=int, help='transport chromatic num', default=0)


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


melody_in = score.parts[args.part]  # partオプションの値を使用して選択

key_diff = get_key_diff(args.file)
    
print(f"key diff: {key_diff}")

beats_per_measure = melody_in.getTimeSignatures()[0].numerator

print(f"beats : {beats_per_measure}")

melody_out = stream.Score()

tempo = melody_in.metronomeMarkBoundaries()[0][-1]

melody_out.insert(0, tempo)

if beats_per_measure == 3:
    melody_out.append(meter.TimeSignature('3/4'))

last_pitch = None # おかしな楽譜だとありえるので例外が出るようにしておく

for measure in melody_in.getElementsByClass(stream.Measure):
    for n in measure.notesAndRests:
        if isinstance(n, note.Note):
            if n.tie and n.tie.type in ["continue", "stop"]:
                lyric = 'ー'
            else:
                lyric = cromatic[(n.pitch.midi + key_diff) % 12]
                                
            new_note = note.Note(pitch=n.pitch.midi,
                                 quarterLength=n.quarterLength,
                                 lyric=lyric)
            new_note.transpose(args.transpose, inPlace=True)
            new_note.tie = n.tie

            melody_out.append(new_note)
        elif isinstance(n, note.Rest):
            melody_out.append(note.Rest(quarterLength=n.quarterLength))


melody_out.write('xml', fp=args.outfile)
