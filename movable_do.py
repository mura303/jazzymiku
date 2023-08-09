import mido
import sys
from common import cromatic
import click


@click.command()
@click.option('--midi', required=True)
@click.option('--key', required=True)
def main(midi, key):

    mid = mido.MidiFile(midi)

    mid.print_tracks()

    notes = []

    for msg in mid.tracks[1]:
        if msg.type == 'note_on' and msg.velocity > 0:
            notes.append(cromatic[(msg.note - int(key)) % 12])

    with open("out.txt", "w") as f:
        f.write(" ".join(notes))


if __name__ == '__main__':
    main()
