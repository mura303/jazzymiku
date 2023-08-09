import sys
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from common import cromatic

def getKashi( notes ):
  key = 0
  r = []

  for msg in notes:
    if msg.type == 'note_on' and msg.velocity > 0:
      r.append(cromatic[(msg.note-key) % 12])

  return r


BAR_TICKS = 480
BEATS = 4

mid_in = mido.MidiFile(sys.argv[1])
track = MidiTrack()
track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

kashi = []
notes_orig=[]
notes_only_do=[]
count=0

for msg in mid_in.tracks[1]:
  print(msg)
  if msg.type == 'note_on' or msg.type == 'note_off':
    notes_orig.append(msg)
    notes_only_do.append( msg.copy(note=60) )
    
    count += msg.time

    
  if count >= BAR_TICKS * BEATS:
    
    track.append( Message('note_off', note=60, time=BAR_TICKS*BEATS) )

    track += notes
    kashi += getKashi( notes )
    kashi += getKashi( notes )
    notes = []
    count = 0

mid_out = MidiFile()
mid_out.tracks.append(track)
mid_out.save('new_song.mid')

with open("solfe_kashi.txt", "w") as f:
  f.write("".join(kashi))


#mid = mido.MidiFile(sys.argv[1])

#mid.print_tracks()
