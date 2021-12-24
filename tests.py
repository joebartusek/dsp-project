import notes_id as NID
import read_audio_file as RAF
from matplotlib import pyplot as plt
import librosa
import librosa.display
import numpy as np
import math

transform = 'CQT'

#fpath = input('\nPlease enter path of file to process: ')
fpath = "test_audio/piano_Dm.wav"

if transform == 'STFT':
    audio = RAF.AudioSignal(filepath = fpath)
    frequencies, times, transform = NID.compute_stft(audio.signal, audio.rate)

elif transform == 'CQT':
    frequencies = [27.5*(2**(i/12)) for i in range(84)]
    samples, sample_rate = librosa.load(fpath)
    transform = np.abs(librosa.cqt(samples, sr=sample_rate, 
                             fmin=librosa.note_to_hz('A0'), n_bins=84, bins_per_octave=12))


peaks = NID.get_peaks(transform, frequencies, 'piano')
notes = NID.freq_to_notes(peaks, frequencies)
NID.notes_readable(notes)
chords = NID.identify_chords(notes)
print(chords)