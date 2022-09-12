import requests
import time
from api_key import API_KEY_ASSEMBLYAI



#******************************************************************
#how we communicate with assemblyai api
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'
#******************************************************************


headers_auth = {'authorization': API_KEY_ASSEMBLYAI}


CHUNK_SIZE = 5242880  # 5MB


#upload the file(output.wav) that we have locally to the assemblyai
def upload(filename):
    def read_file(filename,CHUNK_SIZE = 5242880):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint, headers=headers_auth, data=read_file(filename))
    audio_url = upload_response.json()['upload_url']
    # print (upload_response.json())
    return(audio_url)
#that gives you the url where your file lives in assemblyai


# transcribe

#extract the url of the audio from the response     
def transcribe(audio_url):    
    #the data that we want assemblyai to transcribe   
    transcript_request = {'audio_url': audio_url}
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers_auth)
    
    job_id =transcript_response.json()['id']
    # print(transcript_response.json())
    #we get the id of the transcription
    #this id used to say to assemblyai that this is the id of my job and to ask if the transcription job is ready or not
    #if it is not ready it will tell you that it still processing if it is ready it will tell you it is completed and this is you transcript
    #this is what we are going to to in the polling
    return job_id

#polling
#keep polling the assemblyai api to see when the transcription is done


def poll(transcript_id):

    #specific to the transcription job submitted
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    #get request 
    polling_response = requests.get(polling_endpoint, headers=headers_auth)
    # print(polling_response.json())
    return polling_response.json()


def get_transcription_result_url(audio_url):
    transcribe_id = transcribe(audio_url)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            print(data)
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
       
            





#save the transcription
def save_transcript(audio_url,filename):
    data, error = get_transcription_result_url(audio_url)
    
    if data:
        text_filename = filename + '.txt'
        with open(text_filename, 'w') as f:
            f.write(data['text'])
        print('Transcript saved!!')
    elif error:
        print("Error!!!", error)


# data,error = get_transcription_result_url(audio_url)        

# print(data)
