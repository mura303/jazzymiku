from music21 import *

# Load the MusicXML file containing the lead sheet
score = converter.parse('testdata/allthethings.musicxml')

# Extract the chords from the lead sheet


for i, measure in enumerate(score.parts[0].getElementsByClass('Measure')):
    x = measure.getElementsByClass('ChordSymbol')
    for xx in x:
        print(xx)

chords = score.recurse().getElementsByClass('ChordSymbol')
for chord in chords:
    print(chord.figure, chord.beatDuration.quarterLength)

