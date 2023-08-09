import mido
import sys

# cromatic = ['do', 'ra', 're', 'me', 'mi', 'fa',
#            'se', 'so', 're', 'ra', 'te', 'ti']
#

cromatic = ['[d Q]', '[r V]', '[r e]', '[m e]', '[m I]', '[f V]',
            '[s e]', '[s Q]', '[l e]', '[l V]', '[t e]', '[t I]']

# #系はこっち[d I] [r I] [f I] [s I] [l I]

mid = mido.MidiFile(sys.argv[1])

mid.print_tracks()

notes = []

for msg in mid.tracks[1]:
  if msg.type == 'note_on' and msg.velocity > 0:
    notes.append(cromatic[(msg.note-int(sys.argv[2])) % 12])

with open("out.txt", "w") as f:
  f.write(" ".join(notes))
