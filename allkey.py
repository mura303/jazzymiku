from music21 import *
from common import cromatic
import pathlib
import sys

score = converter.parse(sys.argv[1])

cantus = score.parts[0]

for i in range(-12, 12):
    new_score = stream.Score()

    for measure in cantus.getElementsByClass(stream.Measure):
        for n in measure.notesAndRests:
            if isinstance(n, note.Note):
                new_score.append(note.Note(n.pitch.midi+i, quarterLength=n.quarterLength,
                                            lyric=n.lyric))
            elif isinstance(n, note.Rest):
                new_score.append(note.Rest(quarterLength=n.quarterLength))

    new_score.write('xml', fp=f"t{i}.musicxml")
