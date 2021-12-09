from scipy.io import wavfile as wav

class AudioSignal:
    """
    Audio signal object
    """
    def __init__(self, filepath):
        self.rate, self.signal = wav.read(filepath)