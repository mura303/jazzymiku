from music21 import *
from common import cromatic
import sys

score = converter.parse(sys.argv[1])

solfe_offset = int(sys.argv[3])
pitch_offset = int(sys.argv[4])
cantus = score.parts[0]


for i, n in enumerate(cantus.recurse().getElementsByClass('Note')):
    n.lyric = cromatic[(n.pitch.midi - solfe_offset) % 12]
    n.pitch.midi += pitch_offset

score.write('xml', fp=sys.argv[2])
