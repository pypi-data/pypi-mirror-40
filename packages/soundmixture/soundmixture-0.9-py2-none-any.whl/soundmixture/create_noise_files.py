import scipy.io.wavfile as wf
import numpy as np
import os

ascii_snek = """\
    --..,_                     _,.--.
       `'.'.                .'`__ O O  `;__.
          '.'.            .'.'`  '---'`  `
            '.`'--....--'`.'
              `'--....--'`
"""

def main():
    print(ascii_snek)
    
def generate_wav_files(outDir,  waveType='noise', numberOfFiles=10):

    if waveType == 'noise':
        for i in range(numberOfFiles):
            data = np.random.uniform(-1,1,44100) # 44100 random samples between -1 and 1
            scaled = np.int16(data/np.max(np.abs(data)) * 32767)
            fname = "{}/noise{}.wav".format(outDir, i) 
            wf.write(fname, 44100, scaled)
    else:
        try:
            for f in os.listdir(outDir):
                if f.endswith('.wav'): 
                    rate, data = wf.read(os.path.join(outDir, f)) 
                    print(f, data.shape)
                    
        except Exception as e: print(e) 

if __name__ == "__main__":
    #main()
    generate_wav_files('data/audio/',  waveType='audio', numberOfFiles=10)

