import click
from music21 import *
from common import cromatic

@click.command()
@click.option('--abc', required=True)
def main(abc):
    # 楽譜を読み込む
    score = converter.parse(abc)
    song_key = score.analyze('key')
    offset = song_key.tonic.midi % 12

    my_score = stream.Score()
    my_score.metadata = score.metadata

    my_part = stream.Part()
    my_part.append(tempo.MetronomeMark(number=120))

    my_score.insert(my_part)

    # 小節ごとに処理する
    for i, measure in enumerate(score.parts[0].getElementsByClass('Measure')):

        dodo = []
        orig = []
        for n in measure.notes:

            n.transpose(12, inPlace=True)
            n.lyric = cromatic[(n.pitch.midi - offset) % 12]

            do_note = note.Note()
            do_note.pitch = pitch.Pitch(song_key.tonic, octave=3)
            do_note.duration = n.duration
            do_note.lyric = n.lyric

            dodo.append(do_note)
            orig.append(n)

        my_part.append(dodo)
        my_part.append(orig)

    my_score.write('musicxml', fp='out.musicxml')


if __name__ == '__main__':
    main()
