import notes_id as NID
import read_audio_file as RAF
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib as mpl
mpl.rcParams['animation.ffmpeg_path'] = r"/usr/local/bin/ffmpeg"


#fpath = input('\nPlease enter path of file to process: ')
fpath = "piano-c4.wav"
audio = RAF.AudioSignal(filepath = fpath)
frequencies, times, signal_stft = NID.compute_stft(audio.signal, audio.rate)
peaks = NID.get_peaks(signal_stft, frequencies)
notes = NID.freq_to_notes(peaks, frequencies)