import notes_id as NID
import read_audio_file as RAF
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib as mpl
mpl.rcParams['animation.ffmpeg_path'] = r"/usr/local/bin/ffmpeg"


#fpath = input('\nPlease enter path of file to process: ')
fpath = "piano-c4-e4.wav"
audio = RAF.AudioSignal(filepath = fpath)


frequencies, times, signal_stft = NID.compute_stft(audio.signal, audio.rate)

lst = NID.get_note_frequencies(signal_stft, frequencies, 'piano')






# INIT_TONE = 440 / 2**4 / 2**(1/24)  # Frequency of a quarter tone below an A0


#local_means = list()
#        f = INIT_TONE
#        i, i_start = 0, 0
#        while (f < frequencies.max()):
#            local_mean = 0
#            i_start = i
#            while (i < f * (2**(1/12)) and i < len(fourrier_t)):
#                local_mean += fourrier_t[i]
#                i += 1
#            if (i != i_start): local_mean /= (i-i_start)
#            local_means += (i-i_start)*[local_mean]
#            f *= (2**(1/2))