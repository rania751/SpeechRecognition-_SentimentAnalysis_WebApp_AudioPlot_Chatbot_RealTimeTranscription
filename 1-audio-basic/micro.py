#python -m pip install pyaudio
# with this code we can access to the micro of your pc and record your voice in a wav file
import pyaudio
import wave

#set up the parameters
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
#monoformat
CHANNELS = 1
RATE = 16000
#create the pyaudio object
p = pyaudio.PyAudio()
 
# starts recording
#create the stream object
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

print("start recording...")

frames = []
seconds = 5
for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
    print(int(RATE / FRAMES_PER_BUFFER * seconds))
    data = stream.read(FRAMES_PER_BUFFER)
    frames.append(data)

print("recording stopped")

#close everything
stream.stop_stream()
stream.close()
p.terminate()

# save the frame object in a wave file
wf = wave.open("output.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)

#combine all the elements in the frames list into a binary stream 
wf.writeframes(b''.join(frames))
wf.close()