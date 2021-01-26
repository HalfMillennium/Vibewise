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

os.environ["SPOTIPY_CLIENT_ID"] = '9013dc5d86b84ffca62df2f22e00968e'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'b9484118ab374707925b1b15100cc58b'
os.environ["SPOTIPY_REDIRECT_URI"] = 'https://github.com/HalfMillennium'

app = Flask(__name__)

## TODO: Also pass auth token here, for use when queing songs in 'add_to_queue'
@app.route('/getfilter/<path:varargs>', methods=['GET'])
def get_playlist(varargs=None):
    # grab playlist ID and mood from request
    args = varargs.split('/')
    playlist_id = args[0]
    mood = args[1]
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    token = util.prompt_for_user_token("Garrett Chestnut",
                               scope,
                               client_id=os.environ["SPOTIPY_CLIENT_ID"],
                               client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                               redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"])

    sp = spotipy.Spotify(auth=token)
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

    # Now have mood predictions for each song on user's playlist (in english)

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

    # Returns array of songs (IDs) that fit the user's desired mood
    ## TODO: Instead, queue all chosen IDs using auth token provided in request (also a Todo)
    return jsonify(chosen_ids)

@app.route('/gettone/<path:sent>', methods=['GET'])
def get_tone(sent=None):
    # spaces in the string are replaced with '_'
    # Tone Analyzer API
    authenticator = IAMAuthenticator('R7Ja2rP0jp6LucFzOl5-4xbMSVSX5Fci8wc63J0O5-l3')
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )
    sent = sent.replace('_',' ')
    tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/b8f00a45-63d1-4bb9-b1a0-1c2e6bc3e4ca')
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

@app.route('/q', methods=['GET'])
def add_to_queue(token=None):
    # UNNECESSARY -> Chosen IDs already known from 'get_playlist' method

    # NEXT: get token, and queue songs
    return token

if __name__ == '__main__':
    app.run(debug=True)
