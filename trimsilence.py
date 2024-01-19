from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def cut_silence(wav_path, output_path, silence_thresh=-50):
    # WAVファイルを読み込む
    audio = AudioSegment.from_wav(wav_path)

    # 無音区間ではない部分を検出
    nonsilent_parts = detect_nonsilent(audio, silence_thresh=silence_thresh, min_silence_len=100)

    # 無音区間ではない部分だけを結合して新しいオーディオを作成
    if nonsilent_parts:
        start = nonsilent_parts[0][0]
        end = nonsilent_parts[-1][1]
        cut_audio = audio[start:end]
    else:
        cut_audio = audio

    # 新しいファイルとして保存
    cut_audio.export(output_path, format="wav")


input_wav = "input.wav"  # カットしたいWAVファイルへのパス
output_wav = "output.wav"  # 出力するWAVファイルのパス
cut_silence(input_wav, output_wav)
