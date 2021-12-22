import numpy as np
from scipy import signal as ssp
import matplotlib.pyplot as plt
from math import sqrt
#%%
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib as mpl
mpl.rcParams['animation.ffmpeg_path'] = r"/usr/local/bin/ffmpeg"
from time import sleep
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
        * ???? TBD
    """
    
    lowest_tone = 440 / 2**4 / 2**(1/24)  # Frequency of a quarter tone below an A0
    note_frequencies = list()
    length = find_nearest(4200, frequencies)
    
    for t in range(stft.shape[1]):
        fourier_t = abs(stft[:length,t])     
        Y_MAX = fourier_t.max()
        mean = float()
        note_frequencies.append(list())
        threshold = np.zeros(len(fourier_t))
        
        # Compute the overall mean
        for i in fourier_t:
            mean += i**2
        mean /= len(fourier_t.nonzero()[0])
        mean = sqrt(mean)
        
        # Compute mean per four octaves range
        omean = 0
        f = lowest_tone * (2**4)
        l = 0
        l_prev = 0
        while f < frequencies[length]:
            l_prev = l
            while frequencies[l] < f:
                omean += fourier_t[l]**2
                l += 1
            omean /= (l-l_prev)
            omean = sqrt(omean)
            if omean > mean:
                threshold[l_prev:l+1] = 1.5*omean
            else:
                threshold[l_prev:l+1] = 1.5*mean
            f *= 2**4
        threshold[l:] = 1.5*mean
        threshold[:find_nearest(lowest_tone, frequencies)] = fourier_t.max()+1

        plt.figure()
        plt.plot(frequencies[:length], fourier_t,color='b')
        plt.plot(frequencies[:length], threshold,color='m')
        plt.ylim(0,Y_MAX)
        
        # Identify peaks at t
        while not below_threshold(fourier_t, threshold):
            peak = 0
            
            # Identify lowest-frequecy peak
            while (fourier_t[peak] < threshold[peak] or fourier_t[peak+1] > fourier_t[peak]) and peak < len(fourier_t)-1:
                peak += 1
            
            # Add peak to list of frequencies at t
            note_frequencies[t].append(frequencies[peak])
            
            # Remove peak and its harmonics from DFT
            i = peak
            j = 0
            intensity = fourier_t[peak]
            plt.plot(frequencies[peak],intensity,marker='o',color='g')
            while i<len(fourier_t)-2:
                for k in range(i-10,i+11):
                    if k >= len(fourier_t):
                        break
                    fourier_t[k] = max(0, fourier_t[k] - timbre[instrument][j]*intensity)
                if j<len(timbre[instrument])-1:
                    j += 1
                i = find_nearest(frequencies[i]+frequencies[peak], frequencies)
    
            plt.plot(frequencies[:length], fourier_t,color='r')
            plt.ylim(0,Y_MAX)
            
    return note_frequencies
        


def freq_to_notes(note_frequencies):
    """
    TODO
    """
    pass 
#    notes = np.zeros((12*9, len(note_frequencies)))
#    
#    for t in range(len(note_frequencies)):
        
    
    
    
#    fig,ax = plt.subplots()
#    ax.set_xlim(0,frequencies[600])
#    ax.set_ylim(0,abs(stft).max())
#    s_func1, = plt.plot([],[],color='r')
#    s_func2, = plt.plot([],[],color='b')
#    
#    def next_frame(t):
#        s_func1.set_data(frequencies, abs(stft[:,t]))
#        s_func2.set_data(frequencies, all_local_means[t])
#        return [s_func1, s_func2]
#    
#    FuncAnimation(fig,next_frame,frames=range(stft.shape[1]), blit=True, repeat=False)
#    plt.show()