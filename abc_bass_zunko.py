from music21 import *
from common import cromatic
import sys

score = converter.parse(sys.argv[1])

offset = 0
cantus = score.parts[0]

for i, n in enumerate(cantus.recurse().getElementsByClass('Note')):
    n.lyric = cromatic[(n.pitch.midi - offset) % 12]
    n.pitch.midi -= 12

score.write('xml', fp=sys.argv[2])

#score.show()
