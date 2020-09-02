'''Appends spotify features + harmonies to existing lyrical mood data'''
import os
import csv
import spotipy
import spotipy.util as util
import pandas as pd
import ast
import socket
from spotipy.oauth2 import SpotifyOAuth
from musixmatch import Musixmatch
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

os.environ["SPOTIPY_CLIENT_ID"] = '9013dc5d86b84ffca62df2f22e00968e'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'b9484118ab374707925b1b15100cc58b'
os.environ["SPOTIPY_REDIRECT_URI"] = 'https://github.com/HalfMillennium'

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

token = util.prompt_for_user_token("Garrett Chestnut",
                           scope,
                           client_id=os.environ["SPOTIPY_CLIENT_ID"],
                           client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                           redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"])

dataset = pd.read_csv('musix_tone_data.csv')

track_info = dataset.iloc[:,:].values

writer = csv.writer(open('1500_all_features.csv', 'w', encoding='utf-8'))
track_ids = []

song_names = []
all_features = []
all_harmonies = []
labels = []
no_spotify_index = []
obs_count = 0

if token:
    for obs in track_info:
        try:
            sp = spotipy.Spotify(auth=token)
            results = sp.search(q=obs[0].replace(' by ', ' '), limit=1)

            for track in results['tracks']['items']:
                track_ids.append(track['id'])

                # get pitches from Spotify
                aud_analysis = sp.audio_analysis(track['id'])
                all_harmonies.append(aud_analysis['segments'][0]['pitches'])

            if(len(results['tracks']['items']) == 0):
                all_harmonies.append(2)
                no_spotify_index.append(obs_count)
                print(obs[0],"not found on Spotify.")

            song_names.append(obs[0])

        except socket.timeout:
            print("Socket read timeout.")
        obs_count = obs_count + 1
    i = 0
    while(i + 100 < len(track_ids)):
        data = sp.audio_features(track_ids[i:i+100])
        all_features = all_features + data
        i = i + 100

    if(abs(len(track_ids)-i) != 0):
        for val in range(i, len(track_ids)):
            resp = sp.audio_features(track_ids[val])
            all_features.append(resp)
    #print(len(track_ids))

    '''for (i = 0; i < len(all_features); i = i + 1):
        if i in no_spotify_index:
            all_features.insert(i, 2)
            i = i + 1'''
    for val in no_spotify_index:
        all_features.insert(val, 2)
else:
    print("Can't get token for", username)

writer.writerow(["Song","Key","Mode","Danceability","Energy","Valence","Tempo","H1","H2","H3","H4","H5","H6","H7","H8","H9","H10","H11","H12","T-Anger","T-Fear","T-Joy","T-Sadness","T-Analytical","T-Confident","T-Tentative","Mood"])
for song,feat,harmon,tone,label in zip(song_names,all_features,all_harmonies, track_info[:,1:8], track_info[:,-1]):
    if(harmon != 2):
        print(feat)
        try:
            features = [feat[0]['key'],feat[0]['mode'],feat[0]['danceability'],feat[0]['energy'],feat[0]['valence'],feat[0]['tempo']]
        except KeyError as e:
            features = [feat['key'],feat['mode'],feat['danceability'],feat['energy'],feat['valence'],feat['tempo']]

        harmonies = [harmon[0],harmon[1],harmon[2],harmon[3],harmon[4],harmon[5],harmon[6],harmon[7],harmon[8],harmon[9],harmon[10],harmon[11]]
        tones = [tone[0],tone[1],tone[2],tone[3],tone[4],tone[5],tone[6]]
        writer.writerow([song]+features+harmonies+tones+[label])
