import numpy as np
from scipy import signal as ssp
import matplotlib.pyplot as plt
from math import sqrt


#%%

timbre = {
        'piano':    [1.00, 5.00, 1.00, 1.00, 1.00, 0.50, 0.33, 0.10, 0.10, 0.10, 0.10, 1e5],
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
        nperseg = rate * 60*0.25/72
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




def below_threshold(arr, threshold):
    """
    Inputs:
        * Numpy array
        * Threshold numpy array (must be the same length as arr)
    Output:
        * Boolean of whether all elements of arr are lower than all corresponding elements of threshold
    """
    
    if len(arr) == 1:
        return (arr[0] < threshold[0])
    elif arr.max() >= threshold[arr.argmax()]:
        return False
    else:
        return below_threshold(np.concatenate((arr[:arr.argmax()],arr[arr.argmax()+1:])), np.concatenate((threshold[:arr.argmax()],threshold[arr.argmax()+1:])))
    




def get_note_frequencies(stft, frequencies, instrument):
    """
    Inputs:
        * STFT of a signal (shape: (# of frequencies, # of time samples))
        * Array of frequencies of the STFT
    Outputs:
        * ???? TODO
    """
    
    lowest_tone = 440 / 2**4 / 2**(1/24)  # Frequency of a quarter tone below an A0
    note_frequencies = list()
    length = find_nearest(4200, frequencies)
    
    for t in range(stft.shape[1]):
        dft = abs(stft[:length,t])     
        Y_MAX = dft.max()
        mean = float()
        note_frequencies.append(list())
        threshold = np.zeros(len(dft))
        
        # Compute the overall mean
        for i in dft:
            mean += i**2
        mean /= len(dft.nonzero()[0])
        mean = sqrt(mean)
        
        # Compute mean per four octaves range
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

#        plt.figure()
#        plt.plot(frequencies[:length], dft,color='b')
#        plt.plot(frequencies[:length], threshold,color='m')
#        plt.ylim(0,Y_MAX)
        
        # Identify peaks at t
        while not below_threshold(dft, threshold):
            peak = 0
            
            # Identify lowest-frequecy peak
            while (dft[peak] < threshold[peak] or dft[peak+1] > dft[peak]) and peak < len(dft)-1:
                peak += 1
            
            # Add peak to list of frequencies at t
            note_frequencies[t].append(frequencies[peak])
            
            # Remove peak and its harmonics from DFT
            i = peak
            j = 0
            intensity = dft[peak]
#            plt.plot(frequencies[peak],intensity,marker='o',color='g')
            while i<len(dft)-2:
                for k in range(i-10,i+11):
                    if k >= len(dft):
                        break
                    dft[k] = max(0, dft[k] - timbre[instrument][j]*intensity)
                if j<len(timbre[instrument])-1:
                    j += 1
                i = find_nearest(frequencies[i]+frequencies[peak], frequencies)
    
#            plt.plot(frequencies[:length], dft,color='r')
#            plt.ylim(0,Y_MAX)
            
    return note_frequencies








def get_peaks(stft, frequencies):
    lowest_tone = 440 / 2**4  # Frequency of an A0
    peaks = list()
    length = find_nearest(4200, frequencies)
    
    for t in range(stft.shape[1]):
        
        dft = abs(stft[:length,t])     
        Y_MAX = dft.max()
        mean = float()
        threshold = np.zeros(len(dft))
        peaks.append(dict())
        
        # Compute the overall mean
        for i in dft:
            mean += i**2
        mean /= len(dft.nonzero()[0])
        mean = sqrt(mean)
        
        # Compute mean per four octaves range
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
        
        # Clean signal below threshold
        for i in range(length):
            if dft[i] < threshold[i]:
                dft[i] = 0
                
        plt.figure()
        plt.plot(frequencies[:length], dft, color='r')
        
        # Register peaks
        tone = lowest_tone
        left, right = 0, 0
        while left < length:
            left = find_nearest(tone / 2**(1/24), frequencies)
            right = find_nearest(tone * 2**(1/24), frequencies)
            
            if (dft[left:right] != 0).any():
                peaks[t][left+dft[left:right].argmax()] = dft[left:right].max()
                dft[left-1:right+1] = 0
                
            tone *= 2**(1/12)
        
    return peaks








def freq_to_notes(peaks, frequencies):
    """
    TODO
    """
    scale_0 = np.array([16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87])
    notes = np.zeros((12, len(peaks)), dtype=bool)
    
    for t in range(len(peaks)):
        for k,i in peaks[t].items():
            scale = scale_0.copy()
            while scale[-1] < frequencies[k]:
                scale *= 2
            n = find_nearest(frequencies[k], scale)
            notes[n][t] = 1
    
    return notes