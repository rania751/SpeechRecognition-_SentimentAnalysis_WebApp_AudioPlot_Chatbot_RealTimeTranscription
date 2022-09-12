# in the main.py we combine the extractor.py(youtube extractor infos) with assemblyai
# and extract the transcription of the video and also the sentiment classification results
# we will use asseblyai to apply the sentiment classification tasks(assemblyai website=< features=>audio intelligence=>sentiment analysis)
# with sentiment analysis assemblyai can detect the sentiment of each sentence of speech in the audio file
# sentiment analysis return the result of positive , negative , neutral for each sentence in the transcript

import json
import re
from extractor import get_video_info, get_audio_url
from api_comm import save_transcript


def save_video_sentiments(url):
    video_info = get_video_info(url)
    audio_url = get_audio_url(video_info)
    if audio_url:
        title = video_info['title']
        title = title.strip()
        title = re.sub('[^A-Za-z0-9]+', '_', title)
        # title = "data/" + title
        save_transcript(audio_url, title, sentiment_analysis=True)


if __name__ == "__main__":
    # save_video_sentiments("https://youtu.be/e-kSGNzu0hM")
    # save_video_sentiments("https://www.youtube.com/watch?v=DDkA9-kw1eA")

    # with open("Maybe_one_day_Spoken_Word_Poetry_sentiments.json", "r") as f:
    #     data = json.load(f)
    with open("iPhone_13_Review_Pros_and_Cons_sentiments.json", "r") as f:
        data = json.load(f)
   

    positives = []
    negatives = []
    neutrals = []
    for result in data:
        text = result["text"]
        if result["sentiment"] == "POSITIVE":
            positives.append(text)
        elif result["sentiment"] == "NEGATIVE":
            negatives.append(text)
        else:
            neutrals.append(text)

    n_pos = len(positives)
    n_neg = len(negatives)
    n_neut = len(neutrals)

    print("Num positives:", n_pos)
    print("Num negatives:", n_neg)
    print("Num neutrals:", n_neut)

    # ignore neutrals here
    r = n_pos / (n_pos + n_neg)
    print(f"Positive ratio: {r:.3f}")
