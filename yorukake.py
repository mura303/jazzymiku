from music21 import *

# Load the MusicXML file containing the lead sheet
score = converter.parse('yorukake.mxl')

# Extract the chords from the lead sheet

for p in score.parts:
    print(p)

for note in score.parts[0].recurse().notesAndRests:
    print(note.duration.quarterLength)

