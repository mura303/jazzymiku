from pydub import AudioSegment
import argparse

# Function to split a WAV audio file into chunks of 4 seconds
def split_wav_audio(file_path, chunk_length_ms=4000):
    """
    Splits a WAV audio file into chunks of specified length in milliseconds.
    Args:
    - file_path: Path to the WAV audio file.
    - chunk_length_ms: Length of each chunk in milliseconds. Default is 4000ms (4 seconds).
    Returns:
    - A list of AudioSegment objects, each representing a chunk of the original audio.
    """
    audio = AudioSegment.from_wav(file_path)
    chunks = []

    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i+chunk_length_ms]
        chunks.append(chunk)

    return chunks



parser = argparse.ArgumentParser(description='Split WAV audio file into chunks.')
parser.add_argument('file_path', type=str, help='Path to the WAV audio file.')
parser.add_argument('--chunk_length_ms', type=int, default=4000, help='Length of each chunk in milliseconds. Default is 4000ms (4 seconds).')
args = parser.parse_args()

file_path = args.file_path
chunk_length_ms = args.chunk_length_ms

chunks = split_wav_audio(file_path, chunk_length_ms=4000)

# Saving the chunks as separate files
for i, chunk in enumerate(chunks):
    chunk_name = f"chunk_{i+1}.wav"
    chunk.export(chunk_name, format="wav")
    print(f"Chunk {i+1} saved as {chunk_name}")
