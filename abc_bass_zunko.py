from music21 import *
from common import cromatic

score = converter.parse("Yoasobi_-_Racing_into_the_Night.musicxml")

offset = 3
cantus = score.parts[0]

for i, n in enumerate(cantus.recurse().getElementsByClass('Note')):
    n.lyric = cromatic[(n.pitch.midi - offset) % 12]

score.write('xml', fp='yorukake.xml')

#score.show()
