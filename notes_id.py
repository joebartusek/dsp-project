import numpy as np
from scipy import signal as ssp
import matplotlib.pyplot as plt
from math import sqrt

# TODO : remove this
from time import sleep

#%%

timbre = {
        'piano':    [1.00, 1.00, 0.75, 0.75, 0.50, 0.50, 0.33, 0.10, 0.10, 0.10, 0.10, 1e5],
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

#the value of nperseg is currently tailored for our examples, "72" should be the BPM and "60*..." should be 60 times the desired precision (i.e. 0.25 for quarter notes, 0.125 for eighth notes, etc.)




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
    peaks = list()
    length = find_nearest(3520, frequencies)
    tbr = timbre[instrument]
    
    Y_MAX = abs(stft).max()
    
    for t in range(stft.shape[1]):
        
        dft = abs(stft[:length,t])
        mean = float()
        threshold = np.zeros(len(dft))
        peaks.append(dict())
        
        # ---- Compute the overall mean ----
        for i in dft:
            mean += i**2
        mean /= len(dft.nonzero()[0])
        mean = sqrt(mean)
        if mean < Y_MAX/100:
            mean = Y_MAX
        
        # ---- Skip if silence / not loud enough ----
        if dft.max() < mean:
            continue
        
        # ---- Uncomment this if using CQT ----
        threshold = np.full(len(dft), mean)
        
        # ---- Clean dft below threshold and isolate peaks ----
        for pos in range(length):
            if dft[pos] < threshold[pos]:
                dft[pos] = 0
            elif pos < length-1 and dft[pos-1] < dft[pos] and dft[pos] >= dft[pos+1]:
                i = pos
                while dft[i-1] < dft[i]:
                    i -= 1
                dft[i:pos] = 0
                i = pos
                while i < length-1 and dft[i+1] < dft[i]:
                    i += 1
                dft[pos+1:i] = 0
                
#        plt.figure()
#        plt.plot(dft, color='r') #frequencies[:length],
#        plt.ylim(0, Y_MAX)
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
        
#        plt.plot(dft,color='b') #frequencies[:length],
#        plt.ylim(0, Y_MAX)
        
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
    names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    for t in range(notes.shape[0]):
        notes_t = ' '.join([names[n] for n in list(np.where(notes[t,]==1)[0])])
        if notes_t: print(notes_t)
    return



def cyclic_perm(lst):
    lst[:] = lst[1:] + [lst[0]]
    return lst


def identify_chords(notes):
    note_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    chord_types = {
            (7,):        '5',
                        
            (4,7):      '',
            (3,7):      'min',
            (2,7):      'sus2',
            (5,7):      'sus4',
            (3,6):      'dim',
            
            (3,7,10):   'm7',
            (3,7,14):   'mmaj7',
            (4,7,10):   '7',
            (4,7,11):   'maj7',
            (2,7,10):   '7sus2',
            (4,7,10):   '7sus4',
            (3,6,9):    'dim7'
            }
    chord_progression = list()
    
    for t in range(len(notes)):
        if not any(notes[t]):
            continue
        
        seq, intervals = list(), list()
        seq = [n for n in range(12) if notes[t][n]]
        intervals = [(n-seq[0])%12 for n in seq[1:]]
        
        most_likely_chord = str()
        
        for chord_intervals in chord_types.keys():
                        
            perm = 0
            while not all(n in intervals for n in chord_intervals) and perm < len(seq):
                cyclic_perm(seq)
                intervals = [(n-seq[0])%12 for n in seq[1:]]
                perm += 1
            
            if perm == len(seq):
                continue
            else:
                most_likely_chord = note_names[seq[0]] + chord_types[chord_intervals]
    
        chord_progression.append(most_likely_chord)
    
    return chord_progression












        
#        # ---- Compute mean per four octaves range ----
#        omean = 0
#        f = lowest_tone * (2**4)
#        l = 0
#        l_prev = 0
#        while f < frequencies[length]:
#            l_prev = l
#            while frequencies[l] < f:
#                omean += dft[l]**2
#                l += 1
#            omean /= (l-l_prev)
#            omean = sqrt(omean)
#            if omean > mean:
#                threshold[l_prev:l+1] = 1.5*omean
#            else:
#                threshold[l_prev:l+1] = 1.5*mean
#            f *= 2**4
#        threshold[l:] = 1.5*mean
#        threshold[:find_nearest(lowest_tone, frequencies)] = dft.max()+1
