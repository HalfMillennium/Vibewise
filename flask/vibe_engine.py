import os
import csv
import spotipy
import spotipy.util as util
import pandas as pd
import numpy as np
import pickle
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify, request
from sklearn.preprocessing import StandardScaler, LabelEncoder
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import grab_spotify_data as gr

os.environ["SPOTIPY_CLIENT_ID"] = ''
os.environ["SPOTIPY_CLIENT_SECRET"] = ''
os.environ["SPOTIPY_REDIRECT_URI"] = 'https://github.com/HalfMillennium'

app = Flask(__name__)

## TODO: Also pass auth token here, for use when queing songs in 'add_to_queue'
@app.route('/getfilter/', methods=['GET'])
def get_playlist(varargs=None):
    # grab playlist ID, mood and access token from request

    playlist_id = request.args.get('playlist_id')
    mood = request.args.get('mood')
    acc_token = request.args.get('acc')

    app.logger.info("Access: " + acc_token)

    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    sp = spotipy.Spotify(auth=acc_token)
    songs = sp.playlist(playlist_id)
    
    rf_model = pickle.load(open('model_export.sav','rb'))

    # Pass songs and sp to GrabSpotInfo object
    raw_dataset = gr.GrabSpotInfo(sp, songs)
    raw_dataset = raw_dataset.get_data()
    # Convert raw_dataset into dataframe
    X_raw = pd.DataFrame(raw_dataset)

    # Scale values
    sc = StandardScaler()
    X = X_raw.iloc[:,1:].values
    X = sc.fit_transform(X)

    # Load encoder from file
    encoder = pickle.load(open('result_encoder.sav','rb'))
    y_pred = rf_model.predict(X)
    results = encoder.inverse_transform(y_pred)

    # Now have mood predictions for each song on user's playli st (in english)

    merge = []
    for i, track in enumerate(raw_dataset):
        row = []
        for item in track:
            row.append(item)
        row.append(results[i])
        merge.append(row)

    chosen_ids = []
    
    for song in merge:
        if(song[-1] == mood):
            chosen_ids.append(song[0])
    #app.logger.info("Chosen ids:",chosen_ids[0], "Length:",len(chosen_ids))

    # Queue songs to currently playing device
    for track in chosen_ids:
        sp.add_to_queue(track)
    t = sp.tracks(chosen_ids)
    track_info = []
    for song in t:
        track_info.append([song['album']['images'][0]['url'],song['artists'][0]['name'],song['name']])
    current = sp.currently_playing()
    track_info.insert(0, [current['album']['images'][0]['url'],current['artists'][0]['name'],current['name']])
    # Returns array of songs (IDs) that fit the user's desired mood
    return jsonify(track_info)

@app.route('/gettone/<path:sent>', methods=['GET'])
def get_tone(sent=None):
    # spaces in the string are replaced with '_'
    # Tone Analyzer API
    authenticator = IAMAuthenticator('')
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )
    sent = sent.replace('_',' ')
    tone_analyzer.set_service_url('')
    tone_analysis = tone_analyzer.tone(
        {'text': sent },
        content_type='application/json'
    ).get_result()

    return jsonify(derive_mood(tone_analysis['document_tone']['tones']))

# accepts ['tone_a','tone_b'] or ['one_tone']
def derive_mood(tones):
    vals = ['Anger', 'Fear', 'Joy', 'Sadness', 'Analytical', 'Confident', 'Tentative']
    sc = []
    to = []
    for k in tones:
        sc.append(k['score'])
        to.append(k['tone_name'])
    
    sc_len = len(sc)

    if(sc_len < 1):
        return 'no_tone'
    elif(sc_len > 1):
        to = to[-2:]

    if(sc_len > 1):
        if(vals[0] in to and vals[3] in to):
            return 'sad'
        if(vals[0] in to):
            return 'angry'
        if(vals[1] in to and vals[2] in to):
            return 'happy'
        if(vals[1] in to and vals[3] in to):
            return 'sad'
        if(vals[1] in to and vals[4] in to):
            return 'sad'
        if(vals[1] in to and vals[5] in to):
            return 'angry'
        if(vals[2] in to and vals[4] in to):
            return 'happy'
        if(vals[2] in to and vals[5] in to):
            return 'happy'
        if(vals[3] in to):
            return 'sad'
        if(vals[4] in to and vals[5] in to):
            return 'happy'
        else:
            return 'relaxed'
    else:
        if(to[0] == vals[0]):
            return 'angry'
        if(to[0] == vals[1]):
            return 'sad'
        if(to[0] == vals[2]):
            return 'happy'
        if(to[0] == vals[3]):
            return 'sad'
        if(to[0] == vals[4]):
            return 'relaxed'
        if(to[0] == vals[5]):
            return 'happy'
        if(to[0] == vals[6]):
            return 'relaxed'
        return 'relaxed'

if __name__ == '__main__':
    app.run(debug=True)
