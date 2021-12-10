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
        audio.sampling_freq,
        window = 'nuttall',
        nperseg = audio.rate * 15/72,
        noverlap = 0
    )
    
    
#the value of nperseg is tailored for bohemian-atrocity, 72 should be the BPM and 60 should be 15 times the desired precision (i.e. 0.25 for quarter notes, 0.125 for eighth notes, etc.)