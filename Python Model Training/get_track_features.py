import os
import csv
import spotipy
import spotipy.util as util
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import ast

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

dataset = pd.read_csv('MoodyLyrics4Q.csv')

track_info = dataset.iloc[:,1:].values

writer = csv.writer(open('output_features.csv', 'w'))
track_ids = []
all_features = []
labels = []

if token:
    for obs in track_info:
        labels.append(obs[2])
        sp = spotipy.Spotify(auth=token)
        results = sp.search(q=obs[0]+' '+obs[1], limit=1)
        for track in results['tracks']['items']:
            track_ids.append(track['id'])
            #print(track['id'])

    i = 0
    while(i + 100 < len(track_ids)):
        data = sp.audio_features(track_ids[i:i+100])
        all_features = all_features + data
        i = i + 100

    if(abs(len(track_ids)-i) != 0):
        for val in range(i, len(track_ids)):
            resp = sp.audio_features(track_ids[val])
            all_features.append(resp)
    print(len(track_ids))
else:
    print("Can't get token for", username)

for feat,label in zip(all_features,labels):
    writer.writerow([feat[0]['key'],feat[0]['mode'],feat[0]['danceability'],feat[0]['energy'],feat[0]['valence'],feat[0]['tempo']]+[label])
