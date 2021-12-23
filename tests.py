import notes_id as NID
import read_audio_file as RAF
from matplotlib import pyplot as plt


#fpath = input('\nPlease enter path of file to process: ')
fpath = "piano-c4-e5.wav"
audio = RAF.AudioSignal(filepath = fpath)
frequencies, times, signal_stft = NID.compute_stft(audio.signal, audio.rate)
peaks = NID.get_peaks(signal_stft, frequencies, 'piano')
notes = NID.freq_to_notes(peaks, frequencies)
NID.notes_readable(notes)