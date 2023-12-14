import subprocess
import os
import sys
import pathlib

class NeutrinoRunner:
    def __init__(self):
        # 現在のPATHを取得
        current_path = os.environ.get('PATH')

        # 新しいPATHを作成
        neutrinopath = os.path.join(os.path.dirname(__file__), '..\\NEUTRINO\\bin')

        self.mod_path = f"{neutrinopath};{current_path}"
        
        print(self.mod_path)


    def run(self, command):
        """ コマンドラインコマンドを実行し、出力を表示する """
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={'PATH': self.mod_path})
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout.decode())
        if stderr:
            print(stderr.decode())

    def main(self, basename):
        # プロジェクト設定
        NumThreads = 4
        InferenceMode = 3

        # musicXML_to_label設定
        SUFFIX = "musicxml"

        # NEUTRINO設定
        ModelDir = "ZUNDAMON"
        StyleShift = 0

        # NSF設定
        PitchShiftNsf = 0

        # WORLD設定
        PitchShiftWorld = 0
        FormantShift = 1.0
        SmoothPitch = 0.0
        SmoothFormant = 0.0
        EnhanceBreathiness = 0.0

        # InferenceModeに基づく設定
        if InferenceMode == 4:
            NsfModel = "va"
            SamplingFreq = 48
        elif InferenceMode == 3:
            NsfModel = "vs"
            SamplingFreq = 48
        elif InferenceMode == 2:
            NsfModel = "ve"
            SamplingFreq = 24

        # コマンド実行
        print(f"{os.path.basename(__file__)}: start MusicXMLtoLabel")
        self.run(["musicXMLtoLabel.exe", f"score/musicxml/{basename}.{SUFFIX}", f"score/label/full/{basename}.lab", f"score/label/mono/{basename}.lab"])

        print(f"{os.path.basename(__file__)}: start NEUTRINO")
        self.run(["NEUTRINO.exe", f"score/label/full/{basename}.lab", f"score/label/timing/{basename}.lab", f"output/{basename}.f0", f"output/{basename}.melspec", f"model/{ModelDir}/", "-w", f"output/{basename}.mgc", f"output/{basename}.bap", "-n", "1", "-k", str(StyleShift), "-o", str(NumThreads), "-d", str(InferenceMode), "-t"])

        print(f"{os.path.basename(__file__)}: start NSF")
        self.run(["NSF.exe", f"output/{basename}.f0", f"output/{basename}.melspec", f"./model/{ModelDir}/{NsfModel}.bin", f"output/{basename}.wav", "-l", f"score/label/timing/{basename}.lab", "-n", "1", "-p", str(NumThreads), "-s", str(SamplingFreq), "-f", str(PitchShiftNsf), "-t"])

        print(f"{os.path.basename(__file__)}: start WORLD")
        self.run(["WORLD.exe", f"output/{basename}.f0", f"output/{basename}.mgc", f"output/{basename}.bap", f"output/{basename}_world.wav", "-f", str(PitchShiftWorld), "-m", str(FormantShift), "-p", str(SmoothPitch), "-c", str(SmoothFormant), "-b", str(EnhanceBreathiness), "-n", str(NumThreads), "-t"])

        print(f"{os.path.basename(__file__)}: end")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <BASENAME>")
        sys.exit(1)
    
    nr = NeutrinoRunner()
    
    basename = sys.argv[1]
    nr.main(basename)
