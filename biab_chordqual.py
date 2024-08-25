from music21 import *
import pathlib
import sys
import argparse
from common import cromatic, chord_lyric

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Input file to be parsed")
parser.add_argument('outfile', help='outfile')
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


score_in = score.parts[0]
key_diff = get_key_diff(args.file)
beats_per_measure = score_in.getTimeSignatures()[0].numerator
score_out = stream.Score()

tempo = score_in.metronomeMarkBoundaries()[0][-1].clone()
tempo.number = 120

score_out.insert(0, tempo)

if beats_per_measure == 3:
    score_out.append(meter.TimeSignature('3/4'))

for measure in score_in.getElementsByClass(stream.Measure):

    chords = [None,None,None,None,None]

    for n in measure.getElementsByClass('ChordSymbol'):
        chords[int(n.beat)] = n
        #print(f"{n.beat}:{n.commonName}:{n.chordKind}{n.figure}")

    for i in range(1,beats_per_measure+1):
        print(chords[i])

        if chords[i]:
            root = note.Note()
            root.pitch = pitch.Pitch(n.pitches[0], octave=4)
            root.lyric = cromatic[(root.pitch.midi - key_diff) % 12]
            root.duration = duration.Duration()
            root.duration.quarterLength = 0.5
            score_out.append(root)

            chord_type = note.Note()
            chord_type.pitch = pitch.Pitch(n.pitches[0], octave=4)
            chord_type.lyric = chord_lyric.get(n.commonName, chord_lyric.get(n.chordKind, "ワ")) # ワカラン の ワ
            if chord_type.lyric == "ワ":
                print(f"common:{n.commonName}, kind:{n.chordKind}")
                raise("unknown chord type")
            chord_type.duration = duration.Duration()
            chord_type.duration.quarterLength = 0.5
            score_out.append(chord_type)

        else:
            score_out.append(note.Rest(quarterLength=1.0))

score_out.write('xml', fp=args.outfile)
