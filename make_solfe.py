import sys
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from common import cromatic
import click


def get_kashi(notes, key):
    r = []

    for msg in notes:
        if msg.type == 'note_on' and msg.velocity > 0:
            r.append(cromatic[(msg.note - key) % 12])

    return r


BAR_TICKS = 480
BEATS = 4


@click.command()
@click.option('--midi', required=True)
@click.option('--key', required=True)
@click.option('--blank', is_flag=True)
def main(midi, key, blank):
    mid_in = mido.MidiFile(midi)
    track = MidiTrack()
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

    kashi = []
    notes_orig = []
    notes_only_do = []
    count = 0
    do_note = 48 + int(key) % 12

    for msg in mid_in.tracks[1]:
        print(msg)

        if msg.type == 'note_on' or msg.type == 'note_off':
            msg.note = msg.note + 24
            if msg.type == 'note_on' and msg.time > 0: # piaproが連続note_onを認識しないのか、よくわからないがoffを挟めば治る
                notes_orig.append(Message('note_off', note=msg.note, time=msg.time, channel=msg.channel))
                notes_only_do.append(Message('note_off', note=msg.note, time=msg.time, channel=msg.channel))
                notes_orig.append(msg.copy(time=0))
                notes_only_do.append(msg.copy(note=do_note,time=0))
            else:
                notes_orig.append(msg)
                notes_only_do.append(msg.copy(note=do_note))

            count += msg.time

            if count >= BAR_TICKS * BEATS:
                overtime = count - BAR_TICKS * BEATS
                trimmed_time = msg.time - overtime

                notes_orig[-1] = Message('note_off', note=msg.note, time=trimmed_time, channel=msg.channel)
                notes_only_do[-1] = Message('note_off', note=do_note, time=trimmed_time, channel=msg.channel)

                track += notes_only_do

                if blank:
                    track.append(Message('note_off', note=do_note, time=BAR_TICKS * BEATS))

                track += notes_orig

                kashi += get_kashi(notes_orig, int(key))
                kashi += get_kashi(notes_orig, int(key))

                notes_orig = [msg.copy(time=overtime)]
                notes_only_do = [msg.copy(time=overtime, note=do_note)]
                count = overtime

    print("\n\n---\n\n")

    for msg in track:
        print(msg)

    mid_out = MidiFile()
    mid_out.tracks.append(track)
    mid_out.save('new_song.mid')

    with open("solfe_kashi.txt", "w") as f:
        f.write("".join(kashi))


if __name__ == '__main__':
    main()
