#first thing we setup the real time speech recognition with python 
#install the pyaudio to do the micro recording :pip install pyaudio "
#then we use websockets : pip install websocets
#then we use the assembly ai real time speech recognition feature that works over websockets
#then we create the function to send the data from our microphone recording
#and also a function to receive the data 


#websockets is a library for building WebSocket servers and clients in Python with a focus on correctness, simplicity, robustness, and performance.
#Built on top of asyncio, Python’s standard asynchronous I/O framework, it provides an elegant coroutine-based API.

#In computer science, asynchronous I/O is a form of input/output processing that permits other processing to continue before the transmission has finished.

import pyaudio
import websockets
import asyncio
import base64 #incod ethe data to base64 string before the send
import json 
from openai import ask_computer

from api_secret import API_KEY_ASSEMBLYAI

#set up the parameters of the micro
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
#monoformat
CHANNELS = 1
RATE = 16000
#create the pyaudio object
p = pyaudio.PyAudio()
 
#create the stream object
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

# print(p.get_default_input_device_info())


# the AssemblyAI endpoint we're going to hit
#(ps:ws?sample_rate=16000) at the end of the url and we use the same RATE=16000 in the parameters
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


#a funct responsable for sending and receiving the data 
async def send_receive():
    #WE CONNECT TO THE WEBSOCKET WE DO THISa a sync context manager
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", API_KEY_ASSEMBLYAI),),
        ping_interval=5,
        ping_timeout=20
    )as _ws:
        #we try to connect and then we wait for the result
        await asyncio.sleep(0.1)
        session_begins=await _ws.recv()
        print(session_begins)
        print("sending messages")
        

        #two inner functions
        async def send():
            while True:
                try:
                    #we read the microphone input and we specify the frames per buffer"
                    #exception_on_overflow=False when the websocket connection is too slow there might be an overflow  and then we have an exception and we d'ont want this
                    data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                    #then we need to convert and encode it in base64 and decode it again in utf_8 (this is what asemblyai expect)
                    data = base64.b64encode(data).decode("utf-8")
                    #convert it to a json object(a dict with the key audio data(this what assemblyai needs))
                    json_data = json.dumps({"audio_data":str(data)})
                    await _ws.send(json_data)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                await asyncio.sleep(0.01)  

            return True  

        async def receive():
            while True:
                try:
                    # waiting for the transcription result from assemblyai
                    result_str = await _ws.recv()
                    result = json.loads(result_str)
                    # this is a JSON object (a dict in python)
                    #prompt:the transcription of what we set
                    prompt = result['text']
                    #while we are talking it will already start sending the transcript, and once we finished 
                    #our sentence it will do another pass and make a few correction if necessary 
                    #and then we get the final transcript (what we need)
                    if prompt and result['message_type'] == 'FinalTranscript':
                        print("Me:", prompt)
                        answer = ask_computer(prompt)
                        print("Bot", answer)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
        #we need to combine them in a aasync I/O ways
        #to do this we call the gather function
        #it returns two things
        send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(send_receive())

     
        





