import read_audio_file
import numpy as np
from scipy import signal as ssp


def compute_stft(audio): # Length of segments as input ?
    """
    Input: AudioFile object
    Outputs:
        * Array of sample frequencies
        * Array of segment times
        * STFT of AudioFile.signal 
    """
    
    return ssp.stft(
        audio.signal,
        audio.rate,
        window = 'nuttall',
        nperseg = audio.rate * 60*0.125/72,
        noverlap = 0
    )


#the value of nperseg is tailored for bohemian-atrocity, 72 should be the BPM and 15 should be 60 times the desired precision (i.e. 0.25 for quarter notes, 0.125 for eighth notes, etc.)


def get_notes(stft, frequencies):
    """
    Inputs:
        * STFT of a signal (shape: (# of frequencies, # of time samples))
        * Array of frequencies of the STFT
    Output: Array of if notes are played at each time sample
    """

    notes = np.array(12, stft.shape[1])
    
    for t in range(stft.shape[i]):
        fourrier_t = abs(stft[:,t])
    
        local_means = list()
        f = 440 / 2**4 / 2**(1/24)  # Frequency of a quarter tone below an A0
        i, i_start = 0, 0
        while (f < frequencies.max()):
            local_mean = 0
            i_start = i
            while (i < f * (2**(1/12)) and i < len(fourrier_t)):
                local_mean += fourrier_t[i]
                i += 1
            if (i != i_start): local_mean /= (i-i_start)
            local_means += (i-j)*[local_mean]
            f *= (2**(1/2))
        
        