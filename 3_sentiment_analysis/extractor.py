# Sentiment Analysis on iPhone reviews from youtube
# Learning: youtube_dl, sentiment classification feature
# https://youtu.be/e-kSGNzu0hM
#youtube_dl a package used to extract the infos of videos from youtube 
import youtube_dl
from youtube_dl.utils import DownloadError

ydl = youtube_dl.YoutubeDL()

def get_video_info(url):
    with ydl:
        try:
            result = ydl.extract_info(
                url,
                #we could donload the file and then upload it to assemblyai ,
                #But we can skip actually skip the step and just extract the url of the hosted file 
                #and then we can pass it to the transcribe endpoint in assemblyai 
                download=False
               
            )
        except DownloadError:
            return None


    if 'entries' in result:
        # Can be a playlist or a list of videos so we get the first video 
        video_info = result['entries'][0]
    else:
        # Just one video
        video_info = result
        # print(video_info["formats"])
    return video_info
    #we get the whole video info object


def get_audio_url(video_info):
    for f in video_info['formats']:
        #the video start with a lot of diff resolutions we want the m4a extension(the audio format ending)
        # print(f["ext"])
        if f['ext'] == 'm4a':
            return f['url']
    

# if __name__ == '__main__':
#     video_info = get_video_info("https://youtu.be/e-kSGNzu0hM")
#     audio_url=get_audio_url(video_info)
#     print(audio_url)
    #we get the url to this hosted file
    #this url is not related to youtube
    #when we click we have this in the browser so we can listen to the audio file

##=>this is the first part :how to work with the youtube dl package to extract the infos    