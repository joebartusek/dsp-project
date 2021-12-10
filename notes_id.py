import read_audio_file
from scipy import signal as ssp

def compute_stft(audio): # Length of segments as input ?
    """
    Input : AudioFile object
    Outputs :
        * Array of sample frequencies
        * Array of segment times
        * STFT of AudioFile.signal 
    """
    return ssp.stft(
        audio.signal,
        audio.sampling_freq #,
        # WINDOW ?,
        # LENGTH OF SEGMENTS
    )


