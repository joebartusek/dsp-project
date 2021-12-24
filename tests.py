import notes_id as NID
import read_audio_file as RAF
from matplotlib import pyplot as plt
import librosa
import librosa.display
import numpy as np
import math

transform = 'STFT'

#fpath = input('\nPlease enter path of file to process: ')
fpath = "test_audio/piano_DAb.wav"

if transform == 'STFT':
    audio = RAF.AudioSignal(filepath = fpath)
    frequencies, times, signal_stft = NID.compute_stft(audio.signal, audio.rate)
    peaks = NID.get_peaks(signal_stft, frequencies, 'piano')
    notes = NID.freq_to_notes(peaks, frequencies)
    NID.notes_readable(notes)

elif transform == 'CQT':
    audio = RAF.AudioSignal(filepath = fpath)
    frequencies = np.logspace(math.log(27.5,10), math.log(4186,10), 87)
    samples, sample_rate = librosa.load(fpath)
    cqt = np.abs(librosa.cqt(samples, sr=sample_rate, 
                             fmin=librosa.note_to_hz('A0'), n_bins=87, bins_per_octave=12))
    peaks = NID.get_peaks(cqt, frequencies, 'piano')
    notes = NID.freq_to_notes(peaks, frequencies)
    NID.notes_readable(notes)