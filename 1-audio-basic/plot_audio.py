# https://learnpython.com/blog/plot-waveform-in-python/

#with this code we can plot your mono audio
#we get two .png files one to plot the audio and ont to plot the left channel  
import wave
import numpy as np
import matplotlib.pyplot as plt

wav_obj = wave.open('audio1.wav', 'r')

sample_freq = wav_obj.getframerate()
print(sample_freq)

n_samples = wav_obj.getnframes()
print(n_samples)

#calculate the lenght of the signal 
t_audio = n_samples/sample_freq
print(t_audio, "seconds")

#signal_wave is a bits object
signal_wave = wav_obj.readframes(n_samples)

#so we create a numpy array with data type=int16
signal_array = np.frombuffer(signal_wave, dtype=np.int16)
print(signal_array.shape)



# for stereo:
#l_channel = signal_array[0::2]
#r_channel = signal_array[1::2]

if wav_obj.getnchannels() == 2:
    print("Just mono files")
    wav_obj.exit(0)

#object for the x axes (time axis) from 0 to the length of the signal(n_samples/sample_freq=t_audio),n_samples is the nbr eof parameters(it get a sample for each point of time)
times = np.linspace(0, n_samples/sample_freq, num=n_samples)
print(times.shape)


plt.figure(figsize=(15, 5))
plt.plot(times, signal_array)
plt.title('Audio')
plt.ylabel('Signal Value')
plt.xlabel('Time (s)')
plt.xlim(0, t_audio)
plt.show()

plt.figure(figsize=(15, 5))
plt.specgram(signal_array, Fs=sample_freq, vmin=-20, vmax=50)
plt.title('Left Channel')
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')
plt.xlim(0, t_audio)
plt.colorbar()
plt.show()