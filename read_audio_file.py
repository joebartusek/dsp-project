from scipy.io import wavfile as wav

class AudioSignal:
    """
    Audio signal object
    """
    def __init__(self, filepath):
        ate, self.signal = wav.read(filepath)
        self.length = len(self.signal)
        self.sampling_freq = 1/rate
        self.total_time_duration = self.length/rate


#%% Main

filepath = input('Please enter path of file to process: ')
audio = AudioSignal()