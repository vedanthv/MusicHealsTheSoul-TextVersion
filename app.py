# Core
import streamlit as st

# EDA
import pandas as pd
import numpy as np

# Utils
import joblib

# for spotify integration

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random


client_id = '8be5f0367b7a4b54b730b33faa7c1b2c'
client_secret = '0bc78da67fa44fe985c2586aa74d7e1d'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# fxn

pipe_lr = joblib.load(open("emotion_classifier.pkl", 'rb'))


def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results


def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results


playlist_id = '42EL4koTAevxJ4R8IT8OHJ'
# func to extract all track ids


def get_track_ids(playlist_id):
    music_id_list = []
    playlist = sp.playlist(playlist_id)
    # creating a list of track ids of all the songs in the playlist
    for item in playlist['tracks']['items']:
        music_track = item['track']
        music_id_list.append(music_track['id'])
    return music_id_list


track_ids = get_track_ids(playlist_id)


def main():
    st.title("Music heals The Soul")
    menu = ['Home']

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == 'Home':
        st.subheader("Well Crafted songs to Cheer Up your mood")

        with st.form(key="emotion-clf-form"):
            raw_text = st.text_area("Type Here")
            submit_text = st.form_submit_button(label='Submit')

        if submit_text:
            col1, col2 = st.beta_columns(2)

            # Apply fxn here
            prediction = predict_emotions(raw_text)
            with col1:
                if(prediction == 'sadness' or prediction == 'anger' or prediction == 'worry'):
                    st.error(
                        "**You dont look happy today 😔 here is a song to cheer you up!!**")
                    for i in range(1):
                        random.shuffle(track_ids)
                        embed = '<iframe src="https://open.spotify.com/embed/track/{}" width="300" height="400" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'.format(
                            track_ids[i])

                        st.markdown(embed, unsafe_allow_html=True)

                else:
                    st.success(
                        "**Hurray! You seem to be happy today! Enjoy your life:)**")
                    # image = "<img src = 'enjoy.png' />"
                    # st.markdown(image, unsafe_allow_html = True)

            # with col2:
            #     st.success('Prediction Probability')

            #     st.write(probability)

            #     proba_df = pd.DataFrame(probability,columns = pipe_lr.classes_)

            #     st.write(proba_df)
    else:
        st.subheader("About")


if __name__ == '__main__':
    main()
