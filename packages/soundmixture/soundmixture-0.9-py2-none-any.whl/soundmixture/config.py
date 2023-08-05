import os
import sys

class AppConfig:
    _config = {
            'wav_noise_dir':        '/Users/aakazemaa/Developer/permutation/soundmixture/data/noise',
            'wav_audio_dir':        '/Users/aakazemaa/Developer/permutation/soundmixture/data/audio',
            'wav_mixed_dir':        '/Users/aakazemaa/Developer/permutation/soundmixture/data/mixedaudionoise',
    }

    def __getattr__(self, name):
        try:
            return self._config[name] if name in self._config else None
        except KeyError:
            return None

