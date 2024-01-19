from music21 import *
import sys

score = converter.parse(sys.argv[1])


cantus = score.parts[0]



for i, n in enumerate(cantus.recurse().getElementsByClass('Measure')):
    chords = list(n.recurse().getElementsByClass('Harmony'))
    print(f"{i}:{len(chords)}:{chords[0].splitByQua}")
#        print(harmony.quarterLength)
#        print(harmony.offset)
#        print(harmony.figure)
#        print(harmony.pitchedCommonName)
    

#    print(f"Measure number: {i+1}")
#    chord = n.chordify()
 #   for thisChord in chord.recurse().getElementsByClass('Chord'):
  #      print(thisChord.pitchedCommonName)
        