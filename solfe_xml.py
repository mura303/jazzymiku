from music21 import *
from common import cromatic
import sys

score = converter.parse(sys.argv[1])

offset = 0
cantus = score.parts[0]
new_score = stream.Score()

for measure in cantus.getElementsByClass(stream.Measure):
    for n in measure.notesAndRests:
        if isinstance(n, note.Note):
            new_score.append(note.Note('C4', quarterLength=n.quarterLength,
                                       lyric=cromatic[(n.pitch.midi - offset) % 12]))
        elif isinstance(n, note.Rest):
            new_score.append(note.Rest(quarterLength=n.quarterLength))

    for n in measure.notesAndRests:
        if isinstance(n, note.Note):
            new_score.append(note.Note(n.pitch, quarterLength=n.quarterLength,
                                       lyric=cromatic[(n.pitch.midi - offset) % 12]))
        elif isinstance(n, note.Rest):
            new_score.append(note.Rest(quarterLength=n.quarterLength))


new_score.write('xml', fp=sys.argv[2])
