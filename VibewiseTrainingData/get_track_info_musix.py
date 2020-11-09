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

dataset = pd.read_csv('MoodyLyrics4Q.csv')

track_info = dataset.iloc[137:200,1:].values

writer = csv.writer(open('song_features_musix_temp.csv', 'w', encoding='utf-8'))
track_ids = []

song_names = []
all_features = []
all_harmonies = []

labels = []
all_lyric_object = []
all_lyric_tones = []

# MusixMatch API
musixmatch = Musixmatch('3dbbf7d593f0f05ab045dac7b015c430')

# Tone Analyzer API
authenticator = IAMAuthenticator('R7Ja2rP0jp6LucFzOl5-4xbMSVSX5Fci8wc63J0O5-l3')
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)

tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/b8f00a45-63d1-4bb9-b1a0-1c2e6bc3e4ca')

if token:
    for obs in track_info:
        try:
            labels.append(obs[2])
            sp = spotipy.Spotify(auth=token)
            results = sp.search(q=obs[0]+' '+obs[1], limit=1)
            lyrics = musixmatch.matcher_lyrics_get(obs[1], obs[0])

            lyric_body = ''
            for track in results['tracks']['items']:
                track_ids.append(track['id'])

                # get pitches from Spotify
                aud_analysis = sp.audio_analysis(track['id'])
                all_harmonies.append(aud_analysis['segments'][0]['pitches'])
                song_names.append(track['name'] + ' by ' + track['artists'][0]['name'])
                #print(obs[1] + ' by ' + obs[0] + ' (' + obs[2] + '):\n\n', lyrics['message']['body']['lyrics']['lyrics_body'][:-70])
                if(lyrics['message']['header']['status_code'] != 404):
                    lyric_body = lyrics['message']['body']['lyrics']['lyrics_body'][:-70]
                else:
                    print('404 for ' + obs[1] + ' by ' + obs[0])
                #print(track['id'])
            if(lyric_body == ''):
                print('No lyrics available for ' + track['name'] + ' by ' + track['artists'][0]['name'])
                lyric_body = 'none'
            tone_analysis = tone_analyzer.tone(
                {'text': lyric_body},
                content_type='application/json'
            ).get_result()

            lyric_moods = { "anger": 0, "fear": 0, "joy": 0, "sadness": 0, "analytical": 0, "confident": 0, "tentative": 0 }

            print(obs[1] + ' by ' + obs[0] + ' (' + obs[2] + '):\n')
            for tone in tone_analysis['document_tone']['tones']:
                lyric_moods[tone['tone_id']] = tone['score']
                print(tone['tone_id'],':',lyric_moods[tone['tone_id']],'\n')

            all_lyric_tones.append([lyric_moods['anger'],lyric_moods['fear'],lyric_moods['joy'],lyric_moods['sadness'],lyric_moods['analytical'],lyric_moods['confident'],lyric_moods['tentative']])
        except socket.timeout:
            print("Socket read timeout.")

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
else:
    print("Can't get token for", username)

for song,feat,harmon,tone,label in zip(song_names,all_features,all_harmonies, all_lyric_tones, labels):
    features = [feat[0]['key'],feat[0]['mode'],feat[0]['danceability'],feat[0]['energy'],feat[0]['valence'],feat[0]['tempo']]
    harmonies = [harmon[0],harmon[1],harmon[2],harmon[3],harmon[4],harmon[5],harmon[6],harmon[7],harmon[8],harmon[9],harmon[10],harmon[11]]
    tones = [tone[0],tone[1],tone[2],tone[3],tone[4],tone[5],tone[6]]
    writer.writerow([song]+features+harmonies+tones+[label])
