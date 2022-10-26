import sys
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

def getKashi( notes ):
  key = 0
  r = []
  cromatic = ['[d Q]', '[r V]', '[r e]', '[m e]', '[m I]', '[f V]',
              '[s e]', '[s Q]', '[l e]', '[l V]', '[t e]', '[t I]']
  for msg in notes:
    if msg.type == 'note_on' and msg.velocity > 0:
      r.append(cromatic[(msg.note-key) % 12])

  return r


mid_in = mido.MidiFile(sys.argv[1])
track = MidiTrack()
track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

kashi = []
notes=[]
count=0
first_note = True

for msg in mid_in.tracks[1]:
  if msg.type == 'note_on':
    if first_note:
      first_note = False
      msg.time = 0

    if msg.velocity == 0:
      track.append( Message('note_on',  note=60, velocity=127, time=0) )
      track.append( Message('note_off', note=60, time=msg.time) )

    notes.append(msg)
    count += msg.time
    
  if count == 480 * 4:
    track.append( Message('note_off', note=60, time=480*4) )

    track += notes
    kashi += getKashi( notes )
    kashi += getKashi( notes )
    notes = []
    count = 0

mid_out = MidiFile()
mid_out.tracks.append(track)
mid_out.save('new_song.mid')

with open("solfe_kashi.txt", "w") as f:
  f.write(" ".join(kashi))


#mid = mido.MidiFile(sys.argv[1])

#mid.print_tracks()
