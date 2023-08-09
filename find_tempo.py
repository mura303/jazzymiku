from pydub import AudioSegment
import sys
import pathlib
import wave
import librosa

y, sr = librosa.load(sys.argv[1])
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))