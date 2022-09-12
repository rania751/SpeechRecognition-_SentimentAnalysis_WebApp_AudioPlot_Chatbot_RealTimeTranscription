from api_comm import *
#streamlet is a easy way to start build web interfaces for your app specificly for python
# Streamlit is an open-source Python library that makes it easy to create and share beautiful, 
# custom web apps for machine learning and data science. In just a few minutes you can build and deploy powerful data apps. So let's get started! 
#it has a simple apis/libreries
#to install streamline tab: pip install StreamLit (a python library)
#to run streamline tab: python -m streamlit run file.py

import streamlit as st
import json

st.title("Podcast Summaries")
# save_transcript("71de733737a74d4994b0d4d58ebbeafe")
episode_id = st.sidebar.text_input("Episode ID")
button = st.sidebar.button("Download Episode summary", on_click=save_transcript, args=(episode_id,))



def get_clean_time(start_ms):
    seconds = int((start_ms / 1000) % 60)
    minutes = int((start_ms / (1000 * 60)) % 60)
    hours = int((start_ms / (1000 * 60 * 60)) % 24)
    if hours > 0:
        start_t = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        start_t = f'{minutes:02d}:{seconds:02d}'
        
    return start_t



if button:
    filename = episode_id + '_chapters.json'
    print(filename)
    with open(filename, 'r') as f:
        data = json.load(f)

    chapters = data['chapters']
    episode_title = data['episode_title']
    thumbnail = data['thumbnail']
    podcast_title = data['podcast_title']
    audio = data['audio_url']

    st.header(f"{podcast_title} - {episode_title}")
    st.image(thumbnail, width=200)
    st.markdown(f'#### {episode_title}')

    for chp in chapters:
        with st.expander(chp['gist'] + ' - ' + get_clean_time(chp['start'])):
            chp['summary']