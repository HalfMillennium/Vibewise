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
import grab_spotify_data as gr

os.environ["SPOTIPY_CLIENT_ID"] = '9013dc5d86b84ffca62df2f22e00968e'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'b9484118ab374707925b1b15100cc58b'
os.environ["SPOTIPY_REDIRECT_URI"] = 'https://github.com/HalfMillennium'

app = Flask(__name__)

@app.route('/getfilter', methods=['GET'])
def get_playlist():
    req = request.args
    # grab playlist ID from request
    playlist_id = req.get('playlist_id')
    # grab selected mood from request
    mood = req.get('mood')
    #mood = 'happy'
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
            chosen_ids.append[song[0]]

    # Returns array of songs (IDs) that fit the user's desired mood
    return jsonify(chosen_ids)

if __name__ == '__main__':
    app.run(debug=True)
