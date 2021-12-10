import numpy as np
from scipy.io import wavfile as wav

# Note : We need to be careful to input only 16-bit signed MONO .wav files.


class AudioSignal:
    """
    Audio signal object
    """
    def __init__(self, filepath):
        self.rate, self.signal = wav.read(filepath)
        self.normalized_signal = self.signal / max(self.signal)
        self.length = len(self.signal)
        self.sampling_freq = 1/self.rate
        self.total_time_duration = self.length/self.rate