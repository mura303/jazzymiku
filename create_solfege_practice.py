#!/bin/env python
from music21 import *
import sys
import argparse
import random

parser = argparse.ArgumentParser(description='Create solfege practice score from existing score')
parser.add_argument('infile', help='Input MusicXML file')
parser.add_argument('outfile', help='Output MusicXML file')
parser.add_argument('--measures', type=int, default=128, help='Number of measures (default: 128)')
args = parser.parse_args()

# Eb major scale mapping (movable do: Eb=do)
# MIDI number mod 12 to solfege syllable
def midi_to_solfege(midi_num):
    # Eb major scale: Eb(3), F(5), G(7), Ab(8), Bb(10), C(0), D(2)
    pitch_class = midi_num % 12
    solfege_map = {
        3: 'ド',   # Eb
        5: 'レ',   # F
        7: 'ミ',   # G
        8: 'ファ', # Ab
        10: 'ソ',  # Bb
        0: 'ラ',   # C
        2: 'シ',   # D
    }
    return solfege_map.get(pitch_class, '?')

# Parse input MusicXML file
score = converter.parse(args.infile)

# Get all notes from the score
if len(score.parts) > 0:
    part = score.parts[0]
    notes_list = part.flatten().notes

    if len(notes_list) < 4:
        print("Error: Not enough notes in the input file (need at least 4)")
        sys.exit(1)

    # Extract pitches from notes
    pitches = [n.pitch.midi for n in notes_list]

    print(f"Total notes in source: {len(pitches)}")
    print(f"Generating {args.measures} measures...")

    # Create new score
    new_score = stream.Score()
    new_part = stream.Part()

    # Set key signature to Eb major
    eb_major = key.Key('E-')
    new_part.insert(0, eb_major)

    # Copy tempo if exists
    tempo_marks = part.flatten().getElementsByClass(tempo.MetronomeMark)
    if tempo_marks:
        new_part.insert(0, tempo_marks[0])

    # Generate measures (each pattern creates 2 measures: practice + original)
    measure_num = 1
    for pattern_num in range(args.measures):
        # Randomly select starting position for 4 consecutive notes
        max_start = len(pitches) - 4
        start_idx = random.randint(0, max_start)

        # Collect the pattern
        pattern_pitches = []
        pattern_solfege = []
        for i in range(4):
            pitch_midi = pitches[start_idx + i]
            pattern_pitches.append(pitch_midi)
            pattern_solfege.append(midi_to_solfege(pitch_midi))

        # Measure 1: Practice version (all notes on Eb/tonic, with solfege lyrics)
        m1 = stream.Measure(number=measure_num)
        for i in range(4):
            # All notes on Eb4 (MIDI 63)
            n = note.Note(pitch=63, quarterLength=0.5)
            n.lyric = pattern_solfege[i]
            m1.append(n)
        # Add half rest
        r1 = note.Rest(quarterLength=2.0)
        m1.append(r1)
        new_part.append(m1)
        measure_num += 1

        # Measure 2: Original version (original pitches with solfege lyrics)
        m2 = stream.Measure(number=measure_num)
        for i in range(4):
            n = note.Note(pitch=pattern_pitches[i], quarterLength=0.5)
            n.lyric = pattern_solfege[i]
            m2.append(n)
        # Add half rest
        r2 = note.Rest(quarterLength=2.0)
        m2.append(r2)
        new_part.append(m2)
        measure_num += 1

    new_score.append(new_part)

    # Write to MusicXML
    new_score.write('xml', fp=args.outfile)
    print(f"Created solfege practice score: {args.outfile}")
    print(f"Total patterns: {args.measures}")
    print(f"Total measures: {args.measures * 2} (practice + original for each pattern)")

else:
    print("No parts found in input file")
    sys.exit(1)
