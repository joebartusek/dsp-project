import numpy as np
from scipy import signal as ssp
import matplotlib.pyplot as plt
from math import sqrt

# TODO : remove this
from time import sleep

#%%

timbre = {
        'piano':    [1.00, 2.00, 1.00, 1.00, 1.00, 0.50, 0.33, 0.10, 0.10, 0.10, 0.10, 1e5],
        'trumpet':  [1.00, 0.88, 2.31, 3.43, 1.99, 1.55, 1.40, 1.05, 0.80, 0.43, 0.25, 1e5]
        }


def compute_stft(signal, rate):
    """
    Inputs:
        * Signal of single instrument
        * Sampling rate
    Outputs:
        * Array of sample frequencies
        * Array of segment times
        * STFT of AudioFile.signal 
    """
    
    return ssp.stft(
        signal,
        rate,
        window = 'nuttall',
        nperseg = rate * 60*0.125/72
    )

#the value of nperseg is currently tailored for bohemian-atrocity, "72" should be the BPM and "60*..." should be 60 times the desired precision (i.e. 0.25 for quarter notes, 0.125 for eighth notes, etc.)




def find_nearest(value, arr):
    """
    Inputs:
        * Value (float or int) to look for
        * Sorted (!) array
    Outputs:
        * Index of first element in array nearest to value
    """
    
    index = 0
    while index < len(arr)-1 and arr[index] < value:
        index +=1
    if value-arr[index-1] < abs(arr[index]-value):
        return index-1
    else:
        return index




def get_peaks(stft, frequencies, instrument):
    lowest_tone = 440 / 2**4  # Frequency of an A0
    peaks = list()
    length = find_nearest(4200, frequencies)
    tbr = timbre[instrument]
    
    Y_MAX = abs(stft).max()
    
    for t in range(stft.shape[1]):
        
        dft = abs(stft[:length,t])
        mean = float()
        threshold = np.zeros(len(dft))
        peaks.append(dict())
        
        # Compute the overall mean
        for i in dft:
            mean += i**2
        mean /= len(dft.nonzero()[0])
        mean = sqrt(mean)
        if mean < Y_MAX/100:
            mean = Y_MAX
        
        
        # ---- Skip if silence / not loud enough ----
        if dft.max() < mean:
            continue
        
        
        # ---- Compute mean per four octaves range ----
        omean = 0
        f = lowest_tone * (2**4)
        l = 0
        l_prev = 0
        while f < frequencies[length]:
            l_prev = l
            while frequencies[l] < f:
                omean += dft[l]**2
                l += 1
            omean /= (l-l_prev)
            omean = sqrt(omean)
            if omean > mean:
                threshold[l_prev:l+1] = 1.5*omean
            else:
                threshold[l_prev:l+1] = 1.5*mean
            f *= 2**4
        threshold[l:] = 1.5*mean
        threshold[:find_nearest(lowest_tone, frequencies)] = dft.max()+1
        
        
        # ---- Clean dft below threshold and isolate peaks ----
        for pos in range(length):
            if dft[pos] < threshold[pos]:
                dft[pos] = 0
            elif dft[pos-1] < dft[pos] and dft[pos] >= dft[pos+1]:
                i = pos
                while dft[i-1] < dft[i]:
                    i -= 1
                dft[i:pos] = 0
                i = pos
                while dft[i+1] < dft[i]:
                    i += 1
                dft[pos+1:i] = 0
                
        plt.figure()
        plt.plot(dft, color='r') #frequencies[:length],
        plt.ylim(0, Y_MAX)
#        sleep(1)
           
            
        # ---- Register fundamental peaks and remove harmonics ----
        for pos in range(5,length-5):
            if dft[pos]==0:
                continue

            else:
                peaks[t][pos] = (frequencies[pos],dft[pos])
                
                ref_freq,ref_intensity = frequencies[pos], dft[pos]
                freq = ref_freq*2
                i = find_nearest(freq, frequencies)
                j = 0
                
                while i < length-5:
                    for k in range(i-5,i+6):
                        if dft[k] == 0:
                            continue
                        dft[k] = max(0.0, dft[k] - ref_intensity*tbr[j])
                        if dft[k] < threshold[k]:
                            dft[k] = 0

                    freq += ref_freq
                    i = find_nearest(freq, frequencies)
                    if j < len(tbr)-1:
                        j += 1
        
        plt.plot(dft,color='b') #frequencies[:length],
        plt.ylim(0, Y_MAX)
        
    return peaks

 
    



def freq_to_notes(peaks, frequencies):
    """
    TODO
    """
    scale_0 = np.array([16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87, 32.70])
    notes = np.zeros((len(peaks), 12), dtype=bool)
    
    for t in range(len(peaks)):
        for f,i in peaks[t].values():
            scale = scale_0.copy()
            while scale[-1] < f:
                scale *= 2
            n = find_nearest(f, scale)
            notes[t][n%12] = 1
    
    return notes




def notes_readable(notes):
    names = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
    for t in range(notes.shape[0]):
        print("\n--------\nt =",t)
        for n in range(12):
            if notes[t][n]: print(names[n])
    return