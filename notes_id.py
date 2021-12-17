import numpy as np
from scipy import signal as ssp
import matplotlib.pyplot as plt
#%%
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib as mpl
mpl.rcParams['animation.ffmpeg_path'] = r"/usr/local/bin/ffmpeg"
#%%

timbre = {
        'piano':    [1.00, 0.88, 0.21, 0.16, 0.09, 0.07, 0.04, 0.05, 0.04, 0.04, 0.04, 1e5],
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

#the value of nperseg is currently tailored for bohemian-atrocity, 72 should be the BPM and 15 should be 60 times the desired precision (i.e. 0.25 for quarter notes, 0.125 for eighth notes, etc.)


def get_notes(stft, frequencies, instrument):
    """
    Inputs:
        * STFT of a signal (shape: (# of frequencies, # of time samples))
        * Array of frequencies of the STFT
    Outputs:
        * ???? TBD
    """

    #     notes = np.zeros((12, stft.shape[1]))
    
    lowest_tone = 440 / 2**4 / 2**(1/24)  # Frequency of a quarter tone below an A0
    # all_local_means = list()
    note_frequencies = list()
    
    for t in range(30, stft.shape[1]):
        fourrier_t = abs(stft[:,t])
        note_ranges = [0]        
        local_means = list()
        f = lowest_tone
        i, i_start = 0, 0
        
        while f < frequencies.max():
            local_mean = 0
            i_start = i
            while frequencies[i] < f * (2**(1/12)) and i < len(fourrier_t):
                local_mean += fourrier_t[i]
                i += 1
            if (i != i_start):
                local_mean /= (i-i_start)
                local_means += (i-i_start)*[local_mean]
                note_ranges.append(min(note_ranges[-1] + i-i_start, len(fourrier_t)-1))
            f *= (2**(1/2))
        
        # all_local_means.append(local_means)
        
        
        print("NEW_LOOP")
        plt.figure()
        plt.plot(frequencies[:500], fourrier_t[:500])
        plt.plot(frequencies[:500], local_means[:500])
        
        
        
        while fourrier_t.max()>1.5*local_means[fourrier_t.argmax()]:
            peak = 0
            n = 0
            
            while peak==0 and n<len(note_ranges)-1:
                peak = fourrier_t[note_ranges[n]:note_ranges[n+1]].argmax()
                if fourrier_t[peak]<1.5*local_means[note_ranges[n]]:
                    peak = 0
                n += 1
            
            note_frequencies.append(frequencies[peak])
            print(note_frequencies)
            
            
            i = peak
            print(peak)
            j = 0
            intensity = fourrier_t[peak]
            
            while i<len(fourrier_t)-2 and peak!=0:
                for k in range(i-1,i+2):
                    fourrier_t[k] = max(0, fourrier_t[k] - timbre[instrument][j]*intensity)
                if j<len(timbre[instrument])-1:
                    j += 1
                i += peak
    
            plt.figure()
            plt.plot(frequencies[:500], fourrier_t[:500])
            plt.plot(frequencies[:500], local_means[:500])
    
    return note_frequencies
        
    
    
    
    
    
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
    
        
        