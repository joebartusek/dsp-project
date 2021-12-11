import notes_id
import read_audio_file
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib as mpl
mpl.rcParams['animation.ffmpeg_path'] = r"/usr/local/bin/ffmpeg"


#fpath = input('\nPlease enter path of file to process: ')
fpath = "bohemian-atrocity.wav"
audio = AudioSignal(filepath = fpath)


frequencies, times, signal_stft = compute_stft(audio)

S = 150
local_means = list()
f = 440 / 2**4 / 2**(1/24)
i, j = 0, 0
while (f < frequencies.max()):
    local_mean = 0
    j = i
    while (i < f * (2**(1/12)) and i < len(signal_stft)):
        local_mean += abs(signal_stft[i,S])
        i += 1
    if (i!=j): local_mean /= (i-j)
    local_means += (i-j)*[local_mean]
    f *= (2**(1/2))


plt.plot(frequencies,abs(signal_stft[:,S]))
plt.plot(frequencies,local_means)
plt.xscale('log')
plt.figure()
plt.plot(frequencies,[max(0,abs(signal_stft[i,S]) - local_means[i]) for i in range(len(frequencies))])
plt.xscale('log')
plt.show()




#plt.pcolormesh(times, frequencies, abs(signal_stft), vmin=abs(signal_stft).min(), vmax=abs(signal_stft).max())
#plt.title('STFT Magnitude')
#plt.ylabel('Frequency')
#plt.xlabel('Time')
#plt.show()



#fig,ax = plt.subplots()
#ax.set_xlim(0,frequencies[600])
#ax.set_ylim(0,abs(signal_stft).max())
#s_func, = plt.plot([],[],color='r')
#
#def next_frame(t):
#    s_func.set_data(frequencies, abs(signal_stft[:,t]))
#    return s_func,
#
#anim = FuncAnimation(fig,next_frame,frames=range(len(times)), blit=True, repeat=False)
#plt.show()
#
#
#file = "bohemian-frequencies.mp4"
#writervideo = FFMpegWriter(fps=72/15) 
#anim.save(file, writer=writervideo)