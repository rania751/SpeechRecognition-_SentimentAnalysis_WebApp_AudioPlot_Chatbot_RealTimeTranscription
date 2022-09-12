#this code is to transfert the audio from stereo to mono then we plot it


from pydub import AudioSegment
sound = AudioSegment.from_wav("speech-girl.wav")
sound = sound.set_channels(1)
sound.export("speech-girl1.wav", format="wav")


# audio=AudioSegment.from_wav("audio1.wav")
# audio=audio+6
# audio=audio*2
# audio=audio.fade_in(2000)
# audio.export("copy",format="mp3")
# audio2=AudioSegment.from_mp3("copy.mp3")
# print("done")

# from pydub import AudioSegment
# sound = AudioSegment.from_wav("speech-girl.wav")
# sound = sound.set_channels(1)
# sound.export("speech-girl1.wav", format="wav")

# sound1 = AudioSegment.from_wav("speech.wav")
# sound1 = sound1.set_channels(1)
# sound1.export("speech1.wav", format="wav")

# sound2 = AudioSegment.from_wav("audio.wav")
# sound2 = sound2.set_channels(1)
# sound2.export("audio1.wav", format="wav")