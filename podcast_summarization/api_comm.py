import requests
import json
import time
from api_secret import API_KEY_ASSEMBLYAI
from api_secret import API_KEY_LISTENNOTES
#to make the output mor clear
import pprint

#we are going to use assemblyai to create the summaries of the podcasts and we will get this podcasts from listennotes 
#listennotes is a database of podcasts you are able to get all of its informations plus the episods 
#we need to get the id of an episod from listennotes and send it to assemblyai(the id that we need in the application)

#listennotes endpoint, we need the apisod endpoint to get the episod informations


transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'
asseblyai_headers = {"authorization": API_KEY_ASSEMBLYAI,}



listennotes_episode_endpoint = 'https://listen-api.listennotes.com/api/v2/episodes'
headers_listennotes = {'X-ListenAPI-Key': API_KEY_LISTENNOTES,}


#function which get the episod id and give us the url to the podcasts audio file

def get_episod_audio_url(episod_id):
    url = listennotes_episode_endpoint + '/' + episod_id
    response = requests.request('GET', url, headers=headers_listennotes)

    data = response.json()
    # pprint.pprint(data)

    episode_title = data['title']
    thumbnail = data['thumbnail']
    podcast_title = data['podcast']['title']
    audio_url = data['audio']
    return audio_url, thumbnail, podcast_title, episode_title



##we are going to use auto chapters features of assemblyai 

def transcribe(audio_url, auto_chapters):
    transcript_request = {
        'audio_url': audio_url,
        'auto_chapters': auto_chapters
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=asseblyai_headers)
    return transcript_response.json()['id']

        
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=asseblyai_headers)
    return polling_response.json()


def get_transcription_result_url(url, auto_chapters):
    transcribe_id = transcribe(url, auto_chapters)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
            
        print("waiting for 60 seconds")
        time.sleep(60)
        
        
def save_transcript(episode_id):

    #get the url based on the episod_id fromlistennotes and then sned to assemblyai get the audio chapters informations and save it to a file 6
    audio_url, thumbnail, podcast_title, episode_title=get_episod_audio_url(episode_id)
    data, error = get_transcription_result_url(audio_url, auto_chapters=True)

    #deal with the response thet we get from assemblyai
    pprint.pprint(data)
    
    if data:
        filename = episode_id + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])
             
        filename = episode_id + '_chapters.json'
        with open(filename, 'w') as f:
            chapters = data['chapters']

            data = {'chapters': chapters}
            data['audio_url']=audio_url
            data['thumbnail']=thumbnail
            data['podcast_title']=podcast_title
            data['episode_title']=episode_title
            # for key, value in kwargs.items():
            #     data[key] = value

            json.dump(data, f, indent=4)
            print('Transcript saved')
            return True
    elif error:
        print("Error!!!", error)
        return False     
 