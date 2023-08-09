from functools import reduce

import click
import music21
from music21 import *
from common import cromatic, chord_lyric
import xml.etree.ElementTree as ET


@click.command()
@click.option('--xml', required=True)
def main(xml):
    # 楽譜を読み込む
    score = converter.parse(xml)
    tree = ET.parse(xml)
    for elem in tree.iter(tag='fifths'):
        offset = 7*int(elem.text) % 12

    song_key = score.analyze('key')
    timesig = score.parts[0].recurse().getElementsByClass('TimeSignature')[0].numerator
    if score.parts[0].recurse().getElementsByClass('TimeSignature')[0].denominator != 4:
        """分母は4を前提。6/8だと変になる。"""
        raise("denominator must be 4")

    my_score = stream.Score()
    my_score.metadata = score.metadata

    my_part = stream.Part()
    my_part.append(tempo.MetronomeMark(number=120))

    my_score.insert(my_part)

    # 小節ごとに処理する
    for i, measure in enumerate(score.parts[0].getElementsByClass('Measure')):
        new_notes = []
        for n in measure.getElementsByClass('ChordSymbol'):
            """ nは必ず4分音符ひとつぶんの長さが設定されているのに注意 """
            root = note.Note()
            root.pitch = pitch.Pitch(n.pitches[0], octave=4)
            root.lyric = cromatic[(root.pitch.midi - offset) % 12]

            d = music21.duration.Duration()

            d.quarterLength = 1.0

            root.duration = d

            chord_type = note.Note()
            chord_type.pitch = pitch.Pitch(n.pitches[0], octave=4)

            chord_type.lyric = chord_lyric.get(n.commonName, chord_lyric.get(n.chordKind, "ワ")) # ワカラン の ワ

            if chord_type.lyric == "ワ":
                print(f"{n.commonName} {n.chordKind}")
                raise("unknown chord type")

            print(f"{n.figure} lyric:{chord_type.lyric} commonName:{n.commonName} chordKind:{n.chordKind}")

            # 一小節に2つ以上コードが書いてあるパターン（バグってるいま）
            if len(new_notes) > 0:
                new_notes[-1].duration.quarterLength -= n.beat-1

            d2 = music21.duration.Duration()
            d2.quarterLength = timesig - reduce(lambda x, y: x + y.duration.quarterLength, new_notes, 0) - d.quarterLength
            chord_type.duration = d2

            new_notes.append(root)
            new_notes.append(chord_type)

        my_part.append(new_notes)

    my_score.write('musicxml', fp='out.musicxml')


if __name__ == '__main__':
    main()
