from music21 import *
from common import cromatic
import sys

score = converter.parse(sys.argv[1])

key = score.analyze('key')
print(f"Key of the song: {key}")

num_sharps_flats = key.sharps
print(f"Number of sharps or flats: {num_sharps_flats}")

offset = -num_sharps_flats


cantus = score.parts[0]

for i, n in enumerate(cantus.recurse().getElementsByClass('Note')):
    n.lyric = cromatic[(n.pitch.midi - offset) % 12]

score.write('xml', fp=sys.argv[2])

#score.show()
