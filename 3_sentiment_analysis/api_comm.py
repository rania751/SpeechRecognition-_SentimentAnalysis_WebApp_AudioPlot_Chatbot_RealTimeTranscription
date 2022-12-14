import requests
import json
import time
from api_secret import API_KEY_ASSEMBLYAI



transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'



headers = {
    "authorization": API_KEY_ASSEMBLYAI,
}



def transcribe(audio_url, sentiment_analysis):
    transcript_request = {
        'audio_url': audio_url,
        'sentiment_analysis': sentiment_analysis
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    return transcript_response.json()['id']

        
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(url, sentiment_analysis):
    transcribe_id = transcribe(url, sentiment_analysis)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
            
        print("waiting for 30 seconds")
        time.sleep(30)
        
        
def save_transcript(url, title, sentiment_analysis=False):
    data, error = get_transcription_result_url(url, sentiment_analysis)
    
    if data:
        filename = title + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])
             
        if sentiment_analysis:   
            filename = title + '_sentiments.json'
            with open(filename, 'w') as f:
                sentiments = data['sentiment_analysis_results']
                json.dump(sentiments, f, indent=4)
        print('Transcript saved')
        return True
    elif error:
        print("Error!!!", error)
        return False