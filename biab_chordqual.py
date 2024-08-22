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

tempo = score_in.metronomeMarkBoundaries()[0][-1]
score_out.insert(0, tempo)

if beats_per_measure == 3:
    score_out.append(meter.TimeSignature('3/4'))

for measure in score_in.getElementsByClass(stream.Measure):
    for n in measure.getElementsByClass('ChordSymbol'):
        print(f"{n.beat}:{n.commonName}:{n.chordKind}{n.figure}")
        import pdb; pdb.set_trace()