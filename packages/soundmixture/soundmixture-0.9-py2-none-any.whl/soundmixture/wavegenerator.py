import logging
import scipy.io.wavfile as wf
import numpy as np
from soundmixture.config import AppConfig
import argparse
import os
from pydub import AudioSegment

wlog = logging.getLogger(__name__)

class WaveGen(object):
    """ Generate mixed noise and audio files using exisiting audio and noise wav files """

    def __init__(self, noisedir, audiodir, outdir, snr):

        self.outdir = outdir
        _noise_gain = self.calculate_noise_gain(snr)
        wlog.info("New mixture using snr {} reducing noise by {}db".format(snr, _noise_gain))

        try:
            # Scale the noise files using SNR factor and write the scaled files to scaled directory
            for counter, f in enumerate(os.listdir(noisedir)):
                if f.endswith('.wav'): 
                    _, data = wf.read(os.path.join(noisedir, f)) 
                    scaled = np.int16(data/np.max(np.abs(data)) * 32767/_noise_gain)
                    fname = "{}/../scaled/noise_scaled_{}.wav".format(noisedir, counter + 1) 
                    wf.write(fname, 44100, scaled)
            # Mix the audio files with the scaled noise files and write them to the output dir.
            for f in os.listdir(audiodir):
                if f.endswith('.wav'): 
                    ndx = f.split('.')[0]
                    scaled_noise_wav = AudioSegment.from_file("{}/../scaled/noise_scaled_{}.wav".format(noisedir, ndx))
                    audio_wav = AudioSegment.from_file("{}/{}.wav".format(audiodir, ndx))
                    mixed_audio_noise_wav = scaled_noise_wav.overlay(audio_wav)
                    mixed_audio_noise_wav.export("{}/mixed_{}.wav".format(outdir, ndx), format='wav')

        except Exception as e: print(e) 

    def get_audio_noise_mixed_files_names(self):
        return '\naudio/noise mixed files are:\n{}'.format(
                '\n'.join([os.path.join(self.outdir, f) for f in os.listdir(self.outdir)]))

    @staticmethod
    def calculate_noise_gain(snr):
        return 10 ^ (-1*int(snr)/10)

def generatew():

    parser = argparse.ArgumentParser(description='Generate mixed audio noise files')
    parser.add_argument('noisedir', help='spcefiy where the noise files are located')
    parser.add_argument('audiodir', help='spcefiy where the audio files are located')
    parser.add_argument('mixeddir', help='spcefiy where the output dir for  mixed files audio/noise are located')
    parser.add_argument('SNR', help='spcefiy SNR level')

    wavgenerator = None
    try:
        args = parser.parse_args()
        if not os.path.exists(args.noisedir): raise ValueError("Please specify a valid directory containig noise files") 
        if not os.path.exists(args.audiodir): raise ValueError("Please specify a valid directory containig audio files") 
        if not os.path.exists(args.mixeddir): 
            os.makedirs(args.mixeddir)
        wavgenerator = WaveGen(args.noisedir, args.audiodir, args.mixeddir, args.SNR)
        print(wavgenerator.get_audio_noise_mixed_files_names())

    except Exception as e: 
        print(e) 
    
if __name__ == "__main__":
    generatew()
