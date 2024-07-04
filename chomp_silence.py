from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import sys

# MP3ファイルを読み込む
audio = AudioSegment.from_mp3(sys.argv[1])

# 無音部分を検出するための閾値と時間を設定する（ここでは、無音と判定する閾値を-50dBFS、最短の無音時間を1秒としています）
nonsilent_parts = detect_nonsilent(
    audio,
    min_silence_len=1000,
    silence_thresh=-50
)

# 無音部分がない場合は、オーディオ全体を保持する
if nonsilent_parts:
    start_time, end_time = nonsilent_parts[-1]
    trimmed_audio = audio[:end_time]
else:
    trimmed_audio = audio

# 変更を新しいファイルとして保存
trimmed_audio.export(sys.argv[2], format="mp3")
