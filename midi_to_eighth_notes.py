#!/bin/env python
from music21 import *
import sys
import argparse

parser = argparse.ArgumentParser(description='Convert MIDI to MusicXML with all eighth notes')
parser.add_argument('infile', help='Input MIDI file')
parser.add_argument('outfile', help='Output MusicXML file')
args = parser.parse_args()

# Parse MIDI file
score = converter.parse(args.infile)

# Create new score
new_score = stream.Score()

# Get first part (melody)
if len(score.parts) > 0:
    part = score.parts[0]

    # Create new part
    new_part = stream.Part()

    # Copy tempo if exists
    tempo_marks = part.flatten().getElementsByClass(tempo.MetronomeMark)
    if tempo_marks:
        new_part.insert(0, tempo_marks[0])

    # Get all notes from the original part
    notes = part.flatten().notesAndRests

    # Convert all notes to eighth notes and collect them
    eighth_notes = []
    for n in notes:
        if isinstance(n, note.Note):
            # Create eighth note with same pitch
            eighth_notes.append(n.pitch.midi)
        # Skip rests to only preserve the melody notes

    # Merge consecutive same notes into single eighth note
    if len(eighth_notes) > 0:
        prev_pitch = None

        for pitch in eighth_notes:
            if pitch != prev_pitch:
                # Different pitch, add as eighth note
                new_note = note.Note(pitch=pitch, quarterLength=0.5)
                new_part.append(new_note)
                prev_pitch = pitch
            # If same pitch, skip (don't add duplicate)

    new_score.append(new_part)
else:
    print("No parts found in MIDI file")
    sys.exit(1)

# Write to MusicXML
new_score.write('xml', fp=args.outfile)
print(f"Converted {args.infile} to {args.outfile}")
print(f"Total notes: {len(new_part.flatten().notes)}")
