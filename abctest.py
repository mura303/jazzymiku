from music21 import *

from music21 import *

score = converter.parse("stella.abc")

cantus = score.parts[0]

for i, n in enumerate(cantus.recurse().getElementsByClass('Note')):
    n.lyric = "あほちゃいまんねんぱーでんねん"[i%15]

midi_file = score.write('midi', fp='your_output_midi_file.mid')

#score.show()
